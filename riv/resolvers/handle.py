import datetime
import re

import dateutil
from dateutil.parser import ParserError
from flask import current_app
from idutils.normalizers import normalize_handle
from idutils.validators import is_handle
from invenio_i18n import lazy_gettext as _
from lxml import html
from marshmallow import ValidationError
from marshmallow_utils.fields import EDTFDateString

from ..resolvers import MetadataResolver
from .base import (
    CREATORS_PLACEHOLDER,
    PUBLICATION_DATE_PLACEHOLDER,
    TITLE_PLACEHOLDER,
    ResolverProblem,
    ResolverProblemLevel,
    get_invalid_publication_date_message,
    get_validation_failed_on_date_format_message,
)
from .utils import handle_errors


def parse_date(date):
    error_messages = []

    # 0000 is a special case happening a lot in LINDAT data that passes EDTF schema validation
    if re.match(r"^\d{4}$", date) and not (
        int(date) > 1900 and int(date) <= datetime.datetime.now().year
    ):
        return PUBLICATION_DATE_PLACEHOLDER, [
            get_invalid_publication_date_message(date)
        ]
    try:
        parsed_date = EDTFDateString().deserialize(date)
    except ValidationError:
        try:
            parsed_date = dateutil.parser.parse(date, fuzzy=True)
            parsed_date = datetime.datetime.strftime(parsed_date, "%Y-%m-%d")
            error_messages.append(get_validation_failed_on_date_format_message(date))
        except ParserError:
            error_messages.append(get_invalid_publication_date_message(date))
            parsed_date = PUBLICATION_DATE_PLACEHOLDER
    return parsed_date, error_messages


class HandleResolver(MetadataResolver):
    name = "Handle"

    def can_resolve(self, persistent_url: str) -> bool:
        return is_handle(persistent_url) and (
            "https://hdl.handle.net" in persistent_url
            or "http://hdl.handle.net" in persistent_url
        )

    def resolve(self, persistent_url: str) -> tuple[dict | None, list[ResolverProblem]]:

        handle = normalize_handle(persistent_url)
        handle_url = current_app.config.get("HANDLE_URL")

        response = self.session.get(  # redirect is hardcoded at 3
            url=f"{handle_url}/{handle}"
        )

        if response.status_code != 200:
            if response.status_code == 404:
                return None, [
                    ResolverProblem(
                        resolver=self.name,
                        message=_(
                            "The identifier looks like a Handle, but it was not found in the Handle registry."
                        ),
                        level=ResolverProblemLevel.ERROR,
                    )
                ]
            else:
                return None, [
                    ResolverProblem(
                        resolver=self.name,
                        message=_(
                            "Unexpected error while resolving the Handle. Response returned: %(response)s. ",
                            response=response.content,
                        ),
                        level=ResolverProblemLevel.ERROR,
                    )
                ]

        problem_list = []
        metadata = {}

        tree = html.fromstring(response.content)
        tree = tree.xpath("/html/head")[0]

        metadata["title"] = self.resolve_main_title(tree=tree, problems=problem_list)
        metadata["creators"] = self.resolve_creators(tree=tree, problems=problem_list)
        metadata["publication_date"] = self.resolve_publication_date(
            tree=tree, problems=problem_list
        )
        # there are dataset related tags, dataset_creator, dataset_license, dataset_keyword ..
        # but they are used also on things that aren't datasets
        metadata["resource_type"] = {"id": "other"}

        return metadata, problem_list

    @handle_errors(error_placeholder=TITLE_PLACEHOLDER, alert_user=True)
    def resolve_main_title(self, *, tree, problems):
        titles = tree.xpath('//meta[@name="citation_title"]/@content') or tree.xpath(
            '//meta[@name="title"]/@content'
        )
        if titles:
            return titles[0]
        else:
            problems.append(
                ResolverProblem(
                    resolver=self.name,
                    message=_("Missing title."),
                    level=ResolverProblemLevel.WARNING,
                )
            )
            return TITLE_PLACEHOLDER

    @handle_errors(error_placeholder=CREATORS_PLACEHOLDER, alert_user=True)
    def resolve_creators(self, *, tree, problems):
        creators = tree.xpath('//meta[@name="citation_author"]/@content')
        if not creators:
            problems.append(
                ResolverProblem(
                    resolver=self.name,
                    message=_("Missing creators."),
                    level=ResolverProblemLevel.WARNING,
                )
            )
            return CREATORS_PLACEHOLDER
        creator_list = []

        for creator in creators:
            creator_obj = {}

            creator_type = (
                "personal" if "," in creator else "organizational"
            )  # best guess from looking at LINDAT data
            creator_obj["name"] = creator
            creator_obj["type"] = creator_type

            if creator_type == "personal":
                splt = [part.strip() for part in creator.split(",", 1)]
                creator_obj["given_name"] = splt[1]
                creator_obj["family_name"] = splt[0]

            creator_list.append({"person_or_org": creator_obj})

        return creator_list

    @handle_errors(PUBLICATION_DATE_PLACEHOLDER, alert_user=True)
    def resolve_publication_date(self, *, tree, problems):
        dates = tree.xpath(
            '//meta[@name="citation_publication_date"]/@content'
        ) or tree.xpath('//meta[@name="publication_date"]/@content')

        if not dates:
            problems.append(
                ResolverProblem(
                    resolver=self.name,
                    level=ResolverProblemLevel.WARNING,
                    message=_("Publication date missing."),
                )
            )
            return PUBLICATION_DATE_PLACEHOLDER

        date = dates[0]
        parsed_date, error_messages = parse_date(date)
        for em in error_messages:
            problems.append(
                ResolverProblem(
                    resolver=self.name, level=ResolverProblemLevel.WARNING, message=em
                )
            )
        return parsed_date
