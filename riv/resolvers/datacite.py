from ..resolvers import MetadataResolver
from .base import ResolverProblem, ResolverProblemLevel
from invenio_vocabularies.proxies import current_service as vocabulary_service
from invenio_access.permissions import system_identity
from flask import current_app
from .utils import handle_errors
from marshmallow_utils.fields import EDTFDateString
from marshmallow import ValidationError
from invenio_i18n import lazy_gettext as _
from idutils.validators import is_doi
from idutils.normalizers import normalize_doi

CREATORS_PLACEHOLDER = [{
    "person_or_org": {
        "name": "Unknown Creator",
        "type": "personal",
        "family_name": "Unknown"
    }
}]

PUBLICATION_DATE_PLACEHOLDER = '0000'


class DataciteResolver(MetadataResolver):
    name = "Datacite"

    def can_resolve(self, persistent_url: str) -> bool:

        return is_doi(persistent_url)

    def resolve(self, persistent_url: str) -> (dict | None, list[ResolverProblem]):

        datacite_url = current_app.config.get('DATACITE_URL')
        doi = normalize_doi(persistent_url)
        url = f"{datacite_url}/{doi}"
        response = self.session.get(
            url=url,
        )
        if response.status_code != 200:
            if response.status_code == 404:
                return None, [ResolverProblem(resolver=self.name, message=_(
                    "The identifier looks like a DOI, but it was not found in the DataCite registry."),
                                              level=ResolverProblemLevel.ERROR)]
            else:
                return None, [ResolverProblem(resolver=self.name, message=_(
                    f"Unexpected error while resolving the DOI. DataCite returned: {response.content}. "),
                                              level=ResolverProblemLevel.ERROR)]

        metadata = {}
        problems = []
        data = response.json()
        datacite_metadata = data["data"]["attributes"]

        # (main) title
        # datacite required, rdm required
        datacite_titles = datacite_metadata.get("titles", [])
        main_title = self.resolve_datacite_main_title(titles=datacite_titles, problems=problems)
        metadata["title"] = main_title

        # creators
        # datacite required, rdm required
        datacite_creators = datacite_metadata.get("creators", [])
        creators = self.resolve_datacite_creators(creators=datacite_creators, problems=problems)
        metadata["creators"] = creators

        # publication date
        # datacite required, rdm required
        publication_date = datacite_metadata.get("publicationYear")
        metadata["publication_date"] = self.resolve_datacite_publication_date(publication_date=publication_date,
                                                                              problems=problems)

        # resource type
        # datacite required, rdm required
        datacite_resource_type = datacite_metadata.get("types", {})
        metadata["resource_type"] = {"id": self.resolve_datacite_resource_type(resource_type=datacite_resource_type, problems=problems)}

        return metadata, problems

    @handle_errors(error_placeholder="Unknown title", alert_user=True)
    def resolve_datacite_main_title(self, *, titles, problems):
        for title in titles:
            if 'title' in title and 'titleType' not in title:  # if titleType, it is additional title
                if len(title["title"]) < 3:
                    problems.append(ResolverProblem(resolver=self.name, message=_(
                        "The title is too short. A minimum of 3 characters is required to meet repository requirements."),
                                                    level=ResolverProblemLevel.WARNING))
                    return f'Incompatible title: {title} (please provide a corrected title)'
                return title['title']
        # todo in the documentation it seems that it is possible to have only additional title, test this
        problems.append(
            ResolverProblem(resolver=self.name, message=_("Missing title."),
                            level=ResolverProblemLevel.WARNING))

        return 'Missing title'  # should never happen

    @handle_errors(error_placeholder=CREATORS_PLACEHOLDER, alert_user=True)
    def resolve_datacite_creators(self, *, creators, problems):
        def split_personal_name(name):
            if ',' in name:
                family, given = [part.strip() for part in name.split(',', 1)]
            else:
                family, given = name.strip(), ""
            return family, given

        if len(creators) == 0:
            problems.append(
                ResolverProblem(resolver=self.name, message=_("Missing creators."),
                                level=ResolverProblemLevel.WARNING))
            return CREATORS_PLACEHOLDER

        creator_list = []

        for creator in creators:
            creator_obj = {}

            creator_type = creator.get('nameType', 'personal').lower()
            creator_obj['type'] = creator_type

            given = creator.get('givenName')
            family = creator.get('familyName')
            name = creator.get('name')
            if name is None:
                name = 'Unknown Creator'  # should never happen
                problems.append(
                    ResolverProblem(resolver=self.name, message=_(f"Missing creators name: {creator}."),
                                    level=ResolverProblemLevel.WARNING))

            creator_obj['name'] = name

            if creator_type == 'personal':
                parsed_family, parsed_given = split_personal_name(name)

                family = family or parsed_family
                given = given or (parsed_given if parsed_given else None)

            if given:
                creator_obj['given_name'] = given
            if family:
                creator_obj['family_name'] = family

            creator_list.append({"person_or_org": creator_obj})

        return creator_list

    @handle_errors(PUBLICATION_DATE_PLACEHOLDER)
    def resolve_datacite_publication_date(self, *, publication_date, problems):
        publication_date = str(publication_date)
        edtf_string = EDTFDateString()
        try:
            edtf_string.deserialize(publication_date)
        except ValidationError as e:
            problems.append(
                ResolverProblem(resolver=self.name, message=_(f"Invalid publication date format: {publication_date}."),
                                level=ResolverProblemLevel.WARNING, original_exception=e))
            return PUBLICATION_DATE_PLACEHOLDER
        return publication_date

    @handle_errors('dataset')
    def resolve_datacite_resource_type(self, *, resource_type, problems):
        vocabulary_id = 'resourcetypes'
        _type = resource_type.get("resourceTypeGeneral", "dataset").lower()  # dataset as default option
        try:
            vocabulary_service.read(
                system_identity, (vocabulary_id, _type)
            )
            return _type
        except Exception as e:
            problems.append(
                ResolverProblem(resolver=self.name, message=_(
                    f"The provided resource type {_type} could not be parsed. The default value 'dataset' has been applied."),
                                level=ResolverProblemLevel.WARNING, original_exception=e))
            current_app.logger.exception(
                "Record '%s' was not found in the '%s' vocabulary.",
                _type,
                vocabulary_id
            )
            return "dataset"
