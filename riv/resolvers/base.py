import dataclasses
import datetime
import enum
import re
from collections.abc import Callable
from typing import Protocol, Any

import dateutil
from bs4 import BeautifulSoup
from dateutil.parser import ParserError
from deepmerge import conservative_merger

from flask import current_app
from flask_babel.speaklater import LazyString
from invenio_access.permissions import system_identity
from invenio_i18n import lazy_gettext as _
from marshmallow import ValidationError
from marshmallow_utils.fields import EDTFDateString
from requests.models import Response
from riv.proxies import current_riv_extension
from riv.resolvers.utils import handle_errors
from riv.utils import create_session_with_retries
from invenio_vocabularies.proxies import current_service as vocabulary_service

class ResolverProblemLevel(enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


CREATORS_PLACEHOLDER = [{
    "person_or_org": {
        "name": "Unknown Creator",
        "type": "personal",
        "family_name": "Unknown"
    }
}]
PUBLICATION_DATE_PLACEHOLDER = '1900'
get_validation_failed_on_date_format_message = lambda date: _(f"Publication date format did not pass validation; format: {date}.")
get_invalid_publication_date_message = lambda date: _(f"Invalid publication date format: {date}.")

@dataclasses.dataclass
class ResolverProblem:
    resolver: str
    """Name of the resolver that produced this problem."""

    message: str
    """Human-readable message describing the problem."""

    level: ResolverProblemLevel
    """Severity level of the problem."""

    original_exception: Exception | None = None
    """Original exception that caused the problem, if any."""


# TODO: if level is error -> generate glitchtip issue
# by logger.error(... resolver problem ...)


class UnresolvablePIDError(Exception):
    """Raised when a persistent identifier cannot be resolved to metadata.

    This exception means that all resolvers have failed to resolve the identifier
    - either network problems or the identifier is not supported. User should
    contact support in this case.
    """

    def __init__(self, identifier: str, problems: list[ResolverProblem]):
        self.identifier = identifier
        self.problems = problems
        super().__init__(f"Could not resolve identifier '{identifier}': {problems}.")


class UnsupportedPIDError(Exception):
    """Raised when a persistent identifier is not supported by any resolver.

    This exception means that the identifier format is not recognized by any
    of the configured resolvers. User should check the identifier or contact
    support.
    """

    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Unsupported identifier '{identifier}'.")


class MetadataResolver(Protocol):

    name: str


    identifier_resolve_fn: Callable
    identifier_normalize_fn: Callable
    identifier_code: str
    url: str

    def __init__(self):
        self.session = create_session_with_retries(
            total_retries=4,
            status_forcelist=[403, 429, 500, 502],
        )

    def can_resolve(self, persistent_url: str) -> bool:

        return self.identifier_resolve_fn(persistent_url)

    def _get_response(self, url: str, problems: list[ResolverProblem])->Response | None:

        response = self.session.get(
            url=url,
        )

        if response.status_code != 200:
            if response.status_code == 404:
                problems.append(ResolverProblem(resolver=self.name, message=_(
                    f"The identifier looks like a {self.name}, but it was not found in the DataCite registry."),
                                              level=ResolverProblemLevel.ERROR))
                return None
            else:
                problems.append(ResolverProblem(resolver=self.name, message=_(
                    f"Unexpected error while resolving the identifier. {self.name} resolver returned: {response.content}. "),
                                              level=ResolverProblemLevel.ERROR))
                return None
        return response

    def _get_data_from_response(self, response: Response, problems: list[ResolverProblem])->Any:
        raise NotImplementedError

    def _get_titles(self, data: Any, problems: list[ResolverProblem])->list[str]:
        raise NotImplementedError

    def _get_creators(self, data: Any, problems: list[ResolverProblem])->list[dict[str, Any]]:
        raise NotImplementedError

    def _get_publication_dates(self, data: Any, problems: list[ResolverProblem])->list[str]:
        raise NotImplementedError

    def _get_resource_type(self, data: Any, problems: list[ResolverProblem])->str:
        raise NotImplementedError

    def _process_others(self, data: Any, problems: list[ResolverProblem])->dict[str, Any]:
        return {}

    @handle_errors(error_placeholder="Unknown title", alert_user=True)
    def validate_main_title(self, titles: list[str], problems: list[ResolverProblem])->str:
        if not titles:
            problems.append(
                ResolverProblem(resolver=self.name, message=_("Missing title."),
                                level=ResolverProblemLevel.WARNING, ))
            return "Missing title."

        title = titles[0]
        if len(title) < 3:
            problems.append(ResolverProblem(resolver=self.name, message=_(
                "The title is too short. A minimum of 3 characters is required to meet repository requirements."),
                                            level=ResolverProblemLevel.WARNING))
            return f'Incompatible title: {title} (please provide a corrected title)'

        return title

    @handle_errors(error_placeholder=CREATORS_PLACEHOLDER, alert_user=True)
    def validate_creators(self, creators: list[dict[str, Any]], problems: list[ResolverProblem])->list[dict[str, Any]]:

        if not creators:
            problems.append(
                ResolverProblem(resolver=self.name, message=_("Missing creators."),
                            level=ResolverProblemLevel.WARNING, ))
            return CREATORS_PLACEHOLDER


        return creators

    @handle_errors(PUBLICATION_DATE_PLACEHOLDER, alert_user=True)
    def validate_publication_date(self, dates: list[str | int], problems: list[ResolverProblem])->str:

        if not dates:
            problems.append(ResolverProblem(resolver=self.name, level=ResolverProblemLevel.WARNING, message=_("Publication date missing.")))
            return PUBLICATION_DATE_PLACEHOLDER

        date = dates[0]

        parsed_date, error_messages = parse_date(date)
        for em in error_messages:
            problems.append(ResolverProblem(resolver=self.name, level=ResolverProblemLevel.WARNING, message=em))
        return parsed_date


    @handle_errors('dataset')
    def validate_resource_type(self, resource_type: str, problems: list[ResolverProblem])->dict[str, str]:
        vocabulary_id = 'resourcetypes'
        try:
            vocabulary_service.read(
                system_identity, (vocabulary_id, resource_type)
            )
            return {"id": resource_type}
        except Exception as e:
            problems.append(
                ResolverProblem(resolver=self.name, message=_(
                    f"The provided resource type {resource_type} could not be parsed. The default value 'dataset' has been applied."),
                                level=ResolverProblemLevel.WARNING, original_exception=e))
            current_app.logger.exception(
                "Record '%s' was not found in the '%s' vocabulary.",
                resource_type,
                vocabulary_id
            )
            return {"id": "dataset"}


    def resolve(self, persistent_url: str) -> (dict | None, list[ResolverProblem]):

        identifier = self.identifier_normalize_fn(persistent_url)
        url = f"{self.url}/{identifier}"
        problems = []
        response = self._get_response(
            url=url, problems=problems
        )
        if not response:
            return None, problems
        data = self._get_data_from_response(response, problems)
        if not data:
            return None, problems

        metadata = {}
        metadata["title"] = self.validate_main_title(self._get_titles(data, problems), problems)
        metadata["creators"] = self.validate_creators(self._get_creators(data, problems), problems)
        metadata["publication_date"] = self.validate_publication_date(self._get_publication_dates(data, problems), problems)
        metadata["resource_type"] = self.validate_resource_type(self._get_resource_type(data, problems), problems)

        conservative_merger.merge(metadata, self._process_others(data, problems))

        return metadata, problems


def resolve_record_data(persistent_url: str) -> (dict | None, list[ResolverProblem]):
    """Resolve metadata by persistent url.

    If the metadata can not be resolved, returns (None, "error_message").
    If the metadata is resolved, returns (metadata_dict, "warning message").
    Raises ValueError if all resolvers fail (for now)

        The first resolver that returns metadata wins and its problems are returned.

        If no resolver succeeds, the collected problems from all resolvers are returned.
    """

    resolvers = current_riv_extension.persistent_identifiers_resolvers
    collected_messages: list[ResolverProblem] = []
    can_be_resolved = False
    for resolver in resolvers:
        try:
            if not resolver.can_resolve(persistent_url):
                continue
            can_be_resolved = True
            id_ = f"{resolver.identifier_code}:{resolver.identifier_normalize_fn(persistent_url)}"
            metadata, problems = resolver.resolve(persistent_url)
            record_data = {"id": id_, "metadata": metadata or {}}
        except Exception as e:
            current_app.logger.exception("Exception calling resolver %s", resolver)
            problems = [
                ResolverProblem(
                    resolver=resolver.name,
                    message=_(
                        "An unexpected error occurred in the resolver '%(resolver)s'.",
                        resolver=resolver.name,
                    ),
                    level=ResolverProblemLevel.ERROR,
                    original_exception=e,
                )
            ]
            record_data = None

        collected_messages.extend(problems)

        if record_data is not None:
            record_data["metadata"]["persistent_url"] = persistent_url
            return record_data, problems
        else:
            if not problems:
                raise ValueError(
                    f"Resolver {resolver} returned no metadata and no problems. "
                    "This is an implementation error and must be fixed."
                )

    if not can_be_resolved:
        raise UnsupportedPIDError(persistent_url)

    raise UnresolvablePIDError(persistent_url, collected_messages)


def parse_date(date: str | int)-> (str, list[str|LazyString]):
    error_messages = []

    date = str(date) # may be int which will cause issues
    # 0000 is a special case happening a lot in LINDAT data that passes EDTF schema validation but fails on mapping
    if re.match(r'^\d{4}$', date) and not (int(date) > 1900 and int(date) <= datetime.datetime.now().year):
        return PUBLICATION_DATE_PLACEHOLDER, [get_invalid_publication_date_message(date)]
    try:
        parsed_date = EDTFDateString().deserialize(date)
    except ValidationError as exc:
        try:
            parsed_date = dateutil.parser.parse(date, fuzzy=True)
            parsed_date = datetime.datetime.strftime(parsed_date, "%Y-%m-%d")
            error_messages.append(get_validation_failed_on_date_format_message(date))
        except ParserError as exc:
            error_messages.append(get_invalid_publication_date_message(date))
            parsed_date = PUBLICATION_DATE_PLACEHOLDER
    return parsed_date, error_messages
