import re
from ..resolvers import MetadataResolver
from .base import ResolverProblem, ResolverProblemLevel
from invenio_vocabularies.proxies import current_service as vocabulary_service
from invenio_access.permissions import system_identity
from flask import current_app
from .utils import handle_errors
from marshmallow_utils.fields import EDTFDateString, EDTFDateTimeString
from marshmallow import ValidationError
from invenio_i18n import lazy_gettext as _
from idutils.validators import is_doi
from idutils.normalizers import normalize_doi
from invenio_rdm_records.services.schemas.metadata import record_personorg_schemes, record_identifiers_schemes, record_related_identifiers_schemes
import langcodes
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
        # url = "https://api.test.datacite.org/dois/10.82433/B09Z-4K37"  # for test
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

        # additional titles
        # not required
        additional_titles = self.resolve_datacite_additional_titles(titles=datacite_titles)
        if additional_titles and type(additional_titles) == list and len(additional_titles) > 0:
            metadata["additional_titles"] = additional_titles

        # creators
        # datacite required, rdm required
        # todo affiliations
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

        # publisher
        # not required
        datacite_publisher = datacite_metadata.get("publisher")
        publisher = self.resolve_datacite_publisher(publisher=datacite_publisher)
        if publisher:
            metadata["publisher"] = publisher

        # subjects
        # not required
        #todo where is the vocabulary?

        # contributors
        # not required
        # todo affilitations
        datacite_contributors = datacite_metadata.get("contributors", [])
        contributors = self.resolve_datacite_contributors(contributors=datacite_contributors)
        if len(contributors) > 0:
            metadata["contributors"] = contributors

        # dates
        # not required
        # todo currently not working
        # datacite_dates = datacite_metadata.get("dates", [])
        # dates = self.resolve_datacite_dates(dates=datacite_dates)
        # if len(dates) > 0:
        #     metadata["dates"] = dates

        # language
        # not required
        # one string in datacite, list of voc in rdm
        datacite_language = datacite_metadata.get("language")
        language = self.resolve_datacite_language(language=datacite_language)
        if language:
            metadata["languages"] = [{"id": language}]

        #related identifiers
        #todo: currently not working

        #descriptions
        # todo: currently not working

        # sizes
        # not required
        # array of text
        datacite_sizes = datacite_metadata.get("sizes", [])
        sizes = self.resolve_datacite_strlist(strlist=datacite_sizes)
        if len(sizes) > 0:
            metadata["sizes"] = sizes

        # format
        # not required
        # array of text
        datacite_formats = datacite_metadata.get("formats", [])
        formats = self.resolve_datacite_strlist(strlist=datacite_formats)
        if len(formats) > 0:
            metadata["formats"] = formats

        # version
        # not required
        datacite_version = datacite_metadata.get("version")
        if datacite_version and type(datacite_version) == str:
            metadata["version"] = datacite_version


        #rights
        # currently not working
        # datacite_rights = datacite_metadata.get("rightsList", [])
        # rights = self.resolve_datacite_rights(rights=datacite_rights)
        # if len(rights) > 0:
        #     metadata["rights"] = rights

        return metadata, problems
    @handle_errors()
    def resolve_datacite_dates(self, dates):
        dates_list = []
        for d in dates:
            date_object = {}
            date = d.get("date")
            if not date:
                continue

            edtf_string = EDTFDateTimeString()
            try:
                edtf_string.deserialize(date)
            except:
                continue
            type = d.get("dateType")
            try:
                vocabulary_service.read(
                    system_identity, ("datetypes", type.lower())
                )
            except:
                continue
            date_object["date"] = date
            date_object["type"] = type.lower()
            dates_list.append(date_object)
        return dates_list


    @handle_errors()
    def resolve_datacite_rights(self, rights):
        rights_list = []
        for r in rights:
            code = r.get("rightsIdentifier")
            if code:
                try:
                    vocabulary_service.read(
                        system_identity, ("licenses", code)
                    )
                except:
                    pass
            rights_list.append({"id": code})
        return rights_list

    @handle_errors()
    def resolve_datacite_strlist(self, strlist):
        parsed_strlist = []
        for s in strlist:
            if type(s) == str and s != "":
                parsed_strlist.append(s)

        return parsed_strlist

    @handle_errors()
    def resolve_datacite_language(self, language):
        try:
            longer_code = langcodes.Language.get(language.lower()).to_alpha3()
            vocabulary_service.read(
                system_identity, ("languages", longer_code)
            )
            return longer_code
        except:
            return None

    @handle_errors()
    def resolve_datacite_publisher(self, publisher):
        if publisher:
            return str(publisher)
        return None

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

    @handle_errors()
    def resolve_datacite_additional_titles(self, titles):
        additional_titles = []
        for title in titles:
            title_obj = {}
            t_type = title.get("titleType")
            if t_type is None: #it is main title
                continue
            t_type = re.sub(r'(?<!^)([A-Z])', r'-\1', t_type).lower()
            try:
                vocabulary_service.read(
                    system_identity, ("titletypes", t_type)
                )
            except:
                continue
            t_title = title.get("title")
            if not t_title or len(t_title) < 3:
                continue
            t_lang = None

            title_obj["title"] = t_title
            title_obj["type"] = {"id": t_type}

            if "lang" in title:
                t_lang = self.resolve_datacite_language(language=title["lang"])
            if t_lang:
                title_obj["lang"] = {"id": t_lang}
            additional_titles.append(title_obj)

        return additional_titles

    @handle_errors()
    def split_personal_name(self, name):
        if ',' in name:
            family, given = [part.strip() for part in name.split(',', 1)]
        else:
            family, given = name.strip(), ""
        return family, given

    @handle_errors(error_placeholder=CREATORS_PLACEHOLDER, alert_user=True)
    def resolve_datacite_creators(self, *, creators, problems):


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
                parsed_family, parsed_given = self.split_personal_name(name)

                family = family or parsed_family
                given = given or (parsed_given if parsed_given else None)

            if given:
                creator_obj['given_name'] = given
            if family:
                creator_obj['family_name'] = family

            name_identifiers = self.resolve_datacite_name_identifiers(
                name_identifiers=creator.get("nameIdentifiers", [])
            )
            if name_identifiers and type(name_identifiers) == list and len(name_identifiers) > 0:
                creator_obj["identifiers"] = name_identifiers
            creator_list.append({"person_or_org": creator_obj})

        return creator_list

    @handle_errors()
    def resolve_datacite_contributors(self, contributors):

        contributor_list = []

        for contributor in contributors or []:
            person = {}

            contributor_type = (contributor.get("nameType") or "Personal").lower()
            person["type"] = contributor_type

            given = contributor.get("givenName")
            family = contributor.get("familyName")
            name = contributor.get("name") or " ".join(
                p for p in [given, family] if p
            )
            person["name"] = name

            if contributor_type == "personal":
                parsed_family, parsed_given = self.split_personal_name(name)
                family = family or parsed_family
                given = given or (parsed_given if parsed_given else None)

            if given:
                person["given_name"] = given
            if family:
                person["family_name"] = family

            name_identifiers = self.resolve_datacite_name_identifiers(
                contributor.get("nameIdentifiers", [])
            )
            if name_identifiers:
                person["identifiers"] = name_identifiers

            entry = {"person_or_org": person}
            contributor_type_id = None
            try:
                role = contributor.get("contributorType").lower()
                vocabulary_service.read(
                    system_identity, ("contributorsroles", role)
                )
                contributor_type_id = role
            except:
                pass
            if contributor_type_id:
                entry["role"] = {"id": contributor_type_id}

            contributor_list.append(entry)

        return contributor_list

    @handle_errors()
    def resolve_datacite_name_identifiers(self,* , name_identifiers):

        identifiers = []
        seen = []
        for ni in name_identifiers or []:
            identifier = ni.get("nameIdentifier")
            if identifier in seen: #needs to be unique
                continue
            seen.append(identifier)
            scheme = ni.get("nameIdentifierScheme")
            if scheme:
                scheme = scheme.lower()

            if not identifier or not scheme or scheme not in record_personorg_schemes:
                continue
            obj = {"identifier": identifier}

            obj["scheme"] = scheme
            identifiers.append(obj)
        return identifiers

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
