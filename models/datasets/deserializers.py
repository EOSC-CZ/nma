from __future__ import annotations

from typing import Any, override

from flask_resources.deserializers.json import JSONDeserializer
from lxml import etree
from lxml.etree import QName
from marshmallow import ValidationError


class DataCiteJSONDeserializer(JSONDeserializer):
    """
    Converts json data in DataCite format to CCMM invenio representation.
    """

    @override
    def deserialize(self, data: str | bytes | bytearray | memoryview | None) -> dict:
        """Deserializes the data into an object."""
        as_json_object = super().deserialize(data)
        if not isinstance(as_json_object, dict):
            raise ValidationError("Expected a JSON object")
        return self._deserialize_json(as_json_object)

    def _deserialize_json(self, data: dict) -> dict:
        from oarepo_related_resources.resolvers import DataciteResolver

        resolver = DataciteResolver()
        resolver.metadata = data
        metadata, problems = resolver.resolve_metadata()
        if problems:
            raise ValidationError(f"Errors during DataCite resolution: {problems}")
        return {
            "metadata": metadata,
            "files": {"enabled": False},
            "media_files": {"enabled": False},
        }


class DataCiteXMLDeserializer(DataCiteJSONDeserializer):
    """
    Converts DataCite XML (kernel-4) to RDM representation.
    Based on schema: https://schema.datacite.org/meta/kernel-4/metadata.xsd

    The implementation at first converts XML to DataCite JSON format,
    and then reuses the DataCiteJSONImporter to convert to RDM format.
    """

    NAMESPACE = {"dc": "http://datacite.org/schema/kernel-4"}

    @override
    def deserialize(
        self, data: str | bytes | bytearray | memoryview | None | etree._Element
    ) -> dict:
        """Deserializes the data into an object."""
        if isinstance(data, str):
            data = etree.fromstring(data.encode("utf-8"))
        elif isinstance(data, (bytes, bytearray, memoryview)):
            data = etree.fromstring(bytes(data))
        elif data is None:
            raise ValidationError("No data provided for deserialization")
        datacite_json = self.convert_datacite_xml_to_json(data)
        return self._deserialize_json(datacite_json)

    def convert_datacite_xml_to_json(self, resource: etree._Element) -> dict:
        """
        Convert a DataCite resource element to JSON representation.

        Args:
            resource: The root resource element from DataCite XML

        Returns:
            Dictionary with DataCite JSON representation
        """
        result: dict[str, Any] = {}

        # AV seems to have a wrong kernel - they use http://datacite.org/schema/kernel-4e
        # get the namespace uri of the resource
        ns_uri = QName(resource).namespace
        if ns_uri and ns_uri != self.NAMESPACE["dc"]:
            # set for just this instance
            self.NAMESPACE = {
                **self.NAMESPACE,
                "dc": ns_uri,
            }

        # Required fields
        result["doi"] = self._get_identifier(resource)
        result["creators"] = self._convert_creators(resource)
        result["titles"] = self._convert_titles(resource)
        result["publisher"] = self._convert_publisher(resource)
        result["publicationYear"] = self._get_publication_year(resource)
        result["types"] = self._convert_resource_type(resource)

        # Optional fields
        if subjects := self._convert_subjects(resource):
            result["subjects"] = subjects

        if contributors := self._convert_contributors(resource):
            result["contributors"] = contributors

        if dates := self._convert_dates(resource):
            result["dates"] = dates

        if language := self._get_language(resource):
            result["language"] = language

        if identifiers := self._convert_identifiers(resource):
            result["identifiers"] = identifiers

        if alternate_identifiers := self._convert_alternate_identifiers(resource):
            result["alternateIdentifiers"] = alternate_identifiers

        if related_identifiers := self._convert_related_identifiers(resource):
            result["relatedIdentifiers"] = related_identifiers

        if version := self._get_version(resource):
            result["version"] = version

        if rights_list := self._convert_rights_list(resource):
            result["rightsList"] = rights_list

        if descriptions := self._convert_descriptions(resource):
            result["descriptions"] = descriptions

        if geo_locations := self._convert_geo_locations(resource):
            result["geoLocations"] = geo_locations

        if funding_references := self._convert_funding_references(resource):
            result["fundingReferences"] = funding_references

        if related_items := self._convert_related_items(resource):
            result["relatedItems"] = related_items

        if container := self._convert_container(resource):
            result["container"] = container

        return result

    def _get_text(self, element: etree._Element | None, xpath: str) -> str | None:
        """Helper to get text from an XPath query."""
        if element is None:
            return None
        result = element.xpath(xpath, namespaces=self.NAMESPACE)
        return result[0] if result else None

    def _get_identifier(self, resource: etree._Element) -> str:
        """Extract the DOI identifier."""
        identifier = resource.xpath("dc:identifier/text()", namespaces=self.NAMESPACE)
        return identifier[0] if identifier else ""

    def _convert_creators(self, resource: etree._Element) -> list:
        """Convert creators element to JSON format."""
        creators = []
        creator_elements = resource.xpath(
            "dc:creators/dc:creator", namespaces=self.NAMESPACE
        )

        for creator_elem in creator_elements:
            creator = self._convert_person_or_org(creator_elem, "creator")
            creators.append(creator)

        return creators

    def _convert_person_or_org(self, element: etree._Element, prefix: str) -> dict:
        """
        Convert a creator or contributor element to JSON format.

        Args:
            element: The creator or contributor element
            prefix: Either 'creator' or 'contributor'
        """
        person = {}

        # Name
        name_elem = element.xpath(f"dc:{prefix}Name", namespaces=self.NAMESPACE)
        if name_elem:
            person["name"] = name_elem[0].text or ""

            # nameType attribute
            name_type = name_elem[0].get("nameType")
            if name_type:
                person["nameType"] = name_type

        # Given name
        given_name = element.xpath("dc:givenName/text()", namespaces=self.NAMESPACE)
        if given_name:
            person["givenName"] = given_name[0]

        # Family name
        family_name = element.xpath("dc:familyName/text()", namespaces=self.NAMESPACE)
        if family_name:
            person["familyName"] = family_name[0]

        # Name identifiers - always include even if empty to match Zenodo format
        name_ids = self._convert_name_identifiers(element)
        person["nameIdentifiers"] = name_ids

        # Affiliations - only include if non-empty to match Zenodo format
        affiliations = self._convert_affiliations(element)
        if affiliations:
            person["affiliation"] = affiliations

        return person

    def _convert_name_identifiers(self, element: etree._Element) -> list:
        """Convert nameIdentifier elements to JSON format."""
        name_ids = []
        name_id_elements = element.xpath("dc:nameIdentifier", namespaces=self.NAMESPACE)

        for name_id_elem in name_id_elements:
            name_id = {}

            if name_id_elem.text:
                name_id["nameIdentifier"] = name_id_elem.text

            if scheme := name_id_elem.get("nameIdentifierScheme"):
                name_id["nameIdentifierScheme"] = scheme

            if scheme_uri := name_id_elem.get("schemeUri"):
                name_id["schemeUri"] = scheme_uri

            if name_id:
                name_ids.append(name_id)

        return name_ids

    def _convert_affiliations(self, element: etree._Element) -> list:
        """Convert affiliation elements to JSON format."""
        affiliations = []
        affiliation_elements = element.xpath(
            "dc:affiliation", namespaces=self.NAMESPACE
        )

        for aff_elem in affiliation_elements:
            affiliation = {}

            if aff_elem.text:
                affiliation["name"] = aff_elem.text

            if aff_id := aff_elem.get("affiliationIdentifier"):
                affiliation["affiliationIdentifier"] = aff_id

            if aff_id_scheme := aff_elem.get("affiliationIdentifierScheme"):
                affiliation["affiliationIdentifierScheme"] = aff_id_scheme

            if scheme_uri := aff_elem.get("schemeUri"):
                affiliation["schemeUri"] = scheme_uri

            if affiliation:
                affiliations.append(affiliation)

        return affiliations

    def _convert_titles(self, resource: etree._Element) -> list:
        """Convert titles element to JSON format."""
        titles = []
        title_elements = resource.xpath("dc:titles/dc:title", namespaces=self.NAMESPACE)

        for title_elem in title_elements:
            title = {}

            if title_elem.text:
                title["title"] = title_elem.text

            if title_type := title_elem.get("titleType"):
                title["titleType"] = title_type

            if lang := title_elem.get("{http://www.w3.org/XML/1998/namespace}lang"):
                title["lang"] = lang

            if title:
                titles.append(title)

        return titles

    def _convert_publisher(self, resource: etree._Element) -> str | None:
        """Convert publisher element to JSON format."""
        publisher_elem = resource.xpath("dc:publisher", namespaces=self.NAMESPACE)

        if not publisher_elem:
            return None

        pub_elem = publisher_elem[0]
        # DataCite JSON format expects just the publisher name as a string
        return pub_elem.text if pub_elem.text else None

    def _get_publication_year(self, resource: etree._Element) -> str | None:
        """Extract publication year."""
        year = resource.xpath("dc:publicationYear/text()", namespaces=self.NAMESPACE)
        # DataCite JSON format expects publication year as a string
        return year[0] if year else None

    def _convert_resource_type(self, resource: etree._Element) -> dict:
        """Convert resourceType element to JSON format."""
        types = {}
        resource_type_elem = resource.xpath(
            "dc:resourceType", namespaces=self.NAMESPACE
        )

        if resource_type_elem:
            rt_elem = resource_type_elem[0]

            # Always include resourceType field, even if empty
            types["resourceType"] = rt_elem.text if rt_elem.text else ""

            if rt_general := rt_elem.get("resourceTypeGeneral"):
                types["resourceTypeGeneral"] = rt_general

        return types

    def _convert_subjects(self, resource: etree._Element) -> list:
        """Convert subjects element to JSON format."""
        subjects = []
        subject_elements = resource.xpath(
            "dc:subjects/dc:subject", namespaces=self.NAMESPACE
        )

        for subj_elem in subject_elements:
            subject = {}

            if subj_elem.text:
                subject["subject"] = subj_elem.text

            if subj_scheme := subj_elem.get("subjectScheme"):
                subject["subjectScheme"] = subj_scheme

            if scheme_uri := subj_elem.get("schemeUri"):
                subject["schemeUri"] = scheme_uri

            if value_uri := subj_elem.get("valueUri"):
                subject["valueUri"] = value_uri

            if class_code := subj_elem.get("classificationCode"):
                subject["classificationCode"] = class_code

            if lang := subj_elem.get("{http://www.w3.org/XML/1998/namespace}lang"):
                subject["lang"] = lang

            if subject:
                subjects.append(subject)

        return subjects

    def _convert_contributors(self, resource: etree._Element) -> list:
        """Convert contributors element to JSON format."""
        contributors = []
        contributor_elements = resource.xpath(
            "dc:contributors/dc:contributor", namespaces=self.NAMESPACE
        )

        for contrib_elem in contributor_elements:
            contributor = self._convert_person_or_org(contrib_elem, "contributor")

            # Add contributor type
            if contrib_type := contrib_elem.get("contributorType"):
                contributor["contributorType"] = contrib_type

            contributors.append(contributor)

        return contributors

    def _convert_dates(self, resource: etree._Element) -> list:
        """Convert dates element to JSON format."""
        dates = []
        date_elements = resource.xpath("dc:dates/dc:date", namespaces=self.NAMESPACE)

        for date_elem in date_elements:
            date = {}

            if date_elem.text:
                date["date"] = date_elem.text

            if date_type := date_elem.get("dateType"):
                date["dateType"] = date_type

            if date_info := date_elem.get("dateInformation"):
                date["dateInformation"] = date_info

            if date:
                dates.append(date)

        return dates

    def _get_language(self, resource: etree._Element) -> str | None:
        """Extract language."""
        language = resource.xpath("dc:language/text()", namespaces=self.NAMESPACE)
        return language[0] if language else None

    def _convert_identifiers(self, resource: etree._Element) -> list:
        """Convert identifier to identifiers list (for backward compatibility)."""
        identifiers = []
        identifier_elem = resource.xpath("dc:identifier", namespaces=self.NAMESPACE)

        if identifier_elem:
            id_elem = identifier_elem[0]
            identifier = {}

            if id_elem.text:
                identifier["identifier"] = id_elem.text

            if id_type := id_elem.get("identifierType"):
                identifier["identifierType"] = id_type

            if identifier:
                identifiers.append(identifier)

        return identifiers

    def _convert_alternate_identifiers(self, resource: etree._Element) -> list:
        """Convert alternateIdentifiers element to JSON format."""
        alt_ids = []
        alt_id_elements = resource.xpath(
            "dc:alternateIdentifiers/dc:alternateIdentifier", namespaces=self.NAMESPACE
        )

        for alt_id_elem in alt_id_elements:
            alt_id = {}

            if alt_id_elem.text:
                alt_id["alternateIdentifier"] = alt_id_elem.text

            if alt_id_type := alt_id_elem.get("alternateIdentifierType"):
                alt_id["alternateIdentifierType"] = alt_id_type

            if alt_id:
                alt_ids.append(alt_id)

        return alt_ids

    def _convert_related_identifiers(self, resource: etree._Element) -> list:
        """Convert relatedIdentifiers element to JSON format."""
        related_ids = []
        related_id_elements = resource.xpath(
            "dc:relatedIdentifiers/dc:relatedIdentifier", namespaces=self.NAMESPACE
        )

        for rel_id_elem in related_id_elements:
            related_id = {}

            if rel_id_elem.text:
                related_id["relatedIdentifier"] = rel_id_elem.text

            if rel_id_type := rel_id_elem.get("relatedIdentifierType"):
                related_id["relatedIdentifierType"] = rel_id_type

            if relation_type := rel_id_elem.get("relationType"):
                related_id["relationType"] = relation_type

            if resource_type_general := rel_id_elem.get("resourceTypeGeneral"):
                related_id["resourceTypeGeneral"] = resource_type_general

            if related_metadata_scheme := rel_id_elem.get("relatedMetadataScheme"):
                related_id["relatedMetadataScheme"] = related_metadata_scheme

            if scheme_uri := rel_id_elem.get("schemeUri"):
                related_id["schemeUri"] = scheme_uri

            if scheme_type := rel_id_elem.get("schemeType"):
                related_id["schemeType"] = scheme_type

            if related_id:
                related_ids.append(related_id)

        return related_ids

    def _convert_sizes(self, resource: etree._Element) -> list:
        """Convert sizes element to JSON format."""
        sizes = []
        size_elements = resource.xpath(
            "dc:sizes/dc:size/text()", namespaces=self.NAMESPACE
        )

        for size in size_elements:
            if size:
                sizes.append(size)

        return sizes

    def _convert_formats(self, resource: etree._Element) -> list:
        """Convert formats element to JSON format."""
        formats = []
        format_elements = resource.xpath(
            "dc:formats/dc:format/text()", namespaces=self.NAMESPACE
        )

        for fmt in format_elements:
            if fmt:
                formats.append(fmt)

        return formats

    def _get_version(self, resource: etree._Element) -> str | None:
        """Extract version."""
        version = resource.xpath("dc:version/text()", namespaces=self.NAMESPACE)
        return version[0] if version else None

    def _convert_rights_list(self, resource: etree._Element) -> list:
        """Convert rightsList element to JSON format."""
        rights_list = []
        rights_elements = resource.xpath(
            "dc:rightsList/dc:rights", namespaces=self.NAMESPACE
        )

        for rights_elem in rights_elements:
            rights = {}

            if rights_elem.text:
                rights["rights"] = rights_elem.text

            # Note: XML uses rightsURI (capital), but JSON uses rightsUri (camelCase)
            if rights_uri := rights_elem.get("rightsURI"):
                rights["rightsUri"] = rights_uri

            # TODO: commented out because we do not have the correct vocabulary
            # items yet
            # if rights_id := rights_elem.get("rightsIdentifier"):
            #     rights["rightsIdentifier"] = rights_id
            #     # Zenodo always includes rightsIdentifierScheme when rightsIdentifier exists
            #     # Set to null if not present to match Zenodo format
            #     rights_id_scheme = rights_elem.get("rightsIdentifierScheme")
            #     rights["rightsIdentifierScheme"] = rights_id_scheme

            if scheme_uri := rights_elem.get("schemeUri"):
                rights["schemeUri"] = scheme_uri

            if lang := rights_elem.get("{http://www.w3.org/XML/1998/namespace}lang"):
                rights["lang"] = lang

            if rights:
                rights_list.append(rights)

        return rights_list

    def _convert_descriptions(self, resource: etree._Element) -> list:
        """Convert descriptions element to JSON format."""
        descriptions = []
        desc_elements = resource.xpath(
            "dc:descriptions/dc:description", namespaces=self.NAMESPACE
        )

        for desc_elem in desc_elements:
            description = {}

            # Get text content (may include <br/> tags)
            text_parts = []
            for item in desc_elem.xpath(".//text()"):
                text_parts.append(item)
            # Join text but preserve non-breaking spaces - only strip regular whitespace
            desc_text = "".join(text_parts)
            # Strip only regular spaces, tabs, and newlines (not non-breaking spaces)
            desc_text = desc_text.strip(" \t\n\r")

            if desc_text:
                description["description"] = desc_text

            if desc_type := desc_elem.get("descriptionType"):
                description["descriptionType"] = desc_type

            if lang := desc_elem.get("{http://www.w3.org/XML/1998/namespace}lang"):
                description["lang"] = lang

            if description:
                descriptions.append(description)

        return descriptions

    def _convert_geo_locations(self, resource: etree._Element) -> list:
        """Convert geoLocations element to JSON format."""
        geo_locations = []
        geo_loc_elements = resource.xpath(
            "dc:geoLocations/dc:geoLocation", namespaces=self.NAMESPACE
        )

        for geo_loc_elem in geo_loc_elements:
            geo_location = {}

            # Place
            place = geo_loc_elem.xpath(
                "dc:geoLocationPlace/text()", namespaces=self.NAMESPACE
            )
            if place:
                geo_location["geoLocationPlace"] = place[0]

            # Point
            point = self._convert_geo_location_point(geo_loc_elem)
            if point:
                geo_location["geoLocationPoint"] = point

            # Box
            box = self._convert_geo_location_box(geo_loc_elem)
            if box:
                geo_location["geoLocationBox"] = box

            # Polygon
            polygons = self._convert_geo_location_polygons(geo_loc_elem)
            if polygons:
                geo_location["geoLocationPolygon"] = polygons

            if geo_location:
                geo_locations.append(geo_location)

        return geo_locations

    def _convert_geo_location_point(self, geo_loc_elem: etree._Element) -> dict | None:
        """Convert geoLocationPoint to JSON format."""
        point_elem = geo_loc_elem.xpath(
            "dc:geoLocationPoint", namespaces=self.NAMESPACE
        )

        if not point_elem:
            return None

        point = {}
        lat = point_elem[0].xpath("dc:pointLatitude/text()", namespaces=self.NAMESPACE)
        lon = point_elem[0].xpath("dc:pointLongitude/text()", namespaces=self.NAMESPACE)

        if lat:
            point["pointLatitude"] = lat[0]
        if lon:
            point["pointLongitude"] = lon[0]

        return point if point else None

    def _convert_geo_location_box(self, geo_loc_elem: etree._Element) -> dict | None:
        """Convert geoLocationBox to JSON format."""
        box_elem = geo_loc_elem.xpath("dc:geoLocationBox", namespaces=self.NAMESPACE)

        if not box_elem:
            return None

        box = {}
        west = box_elem[0].xpath(
            "dc:westBoundLongitude/text()", namespaces=self.NAMESPACE
        )
        east = box_elem[0].xpath(
            "dc:eastBoundLongitude/text()", namespaces=self.NAMESPACE
        )
        south = box_elem[0].xpath(
            "dc:southBoundLatitude/text()", namespaces=self.NAMESPACE
        )
        north = box_elem[0].xpath(
            "dc:northBoundLatitude/text()", namespaces=self.NAMESPACE
        )

        if west:
            box["westBoundLongitude"] = west[0]
        if east:
            box["eastBoundLongitude"] = east[0]
        if south:
            box["southBoundLatitude"] = south[0]
        if north:
            box["northBoundLatitude"] = north[0]

        return box if box else None

    def _convert_geo_location_polygons(self, geo_loc_elem: etree._Element) -> list:
        """Convert geoLocationPolygon elements to JSON format."""
        polygons = []
        polygon_elements = geo_loc_elem.xpath(
            "dc:geoLocationPolygon", namespaces=self.NAMESPACE
        )

        for polygon_elem in polygon_elements:
            polygon_points = []
            point_elements = polygon_elem.xpath(
                "dc:polygonPoint", namespaces=self.NAMESPACE
            )

            for point_elem in point_elements:
                point = {}
                lat = point_elem.xpath(
                    "dc:pointLatitude/text()", namespaces=self.NAMESPACE
                )
                lon = point_elem.xpath(
                    "dc:pointLongitude/text()", namespaces=self.NAMESPACE
                )

                if lat:
                    point["pointLatitude"] = lat[0]
                if lon:
                    point["pointLongitude"] = lon[0]

                if point:
                    polygon_points.append({"polygonPoint": point})

            if polygon_points:
                polygons.append(polygon_points)

        return polygons

    def _convert_funding_references(self, resource: etree._Element) -> list:
        """Convert fundingReferences element to JSON format."""
        funding_refs = []
        funding_ref_elements = resource.xpath(
            "dc:fundingReferences/dc:fundingReference", namespaces=self.NAMESPACE
        )

        for funding_ref_elem in funding_ref_elements:
            funding_ref = {}

            # Funder name
            funder_name = funding_ref_elem.xpath(
                "dc:funderName/text()", namespaces=self.NAMESPACE
            )
            if funder_name:
                funding_ref["funderName"] = funder_name[0]

            # Funder identifier
            funder_id_elem = funding_ref_elem.xpath(
                "dc:funderIdentifier", namespaces=self.NAMESPACE
            )
            if funder_id_elem:
                fid_elem = funder_id_elem[0]
                if fid_elem.text:
                    funding_ref["funderIdentifier"] = fid_elem.text

                if fid_type := fid_elem.get("funderIdentifierType"):
                    funding_ref["funderIdentifierType"] = fid_type

                if scheme_uri := fid_elem.get("schemeUri"):
                    funding_ref["funderIdentifierSchemeUri"] = scheme_uri

            # Award number
            award_num_elem = funding_ref_elem.xpath(
                "dc:awardNumber", namespaces=self.NAMESPACE
            )
            if award_num_elem:
                an_elem = award_num_elem[0]
                if an_elem.text:
                    funding_ref["awardNumber"] = an_elem.text

                if award_uri := an_elem.get("awardUri"):
                    funding_ref["awardUri"] = award_uri

            # Award title
            award_title = funding_ref_elem.xpath(
                "dc:awardTitle/text()", namespaces=self.NAMESPACE
            )
            if award_title:
                funding_ref["awardTitle"] = award_title[0]

            if funding_ref:
                funding_refs.append(funding_ref)

        return funding_refs

    def _convert_related_items(self, resource: etree._Element) -> list:
        """Convert relatedItems element to JSON format."""
        related_items = []
        related_item_elements = resource.xpath(
            "dc:relatedItems/dc:relatedItem", namespaces=self.NAMESPACE
        )

        for rel_item_elem in related_item_elements:
            related_item = {}

            # Relation type
            if relation_type := rel_item_elem.get("relationType"):
                related_item["relationType"] = relation_type

            # Related item type
            if rel_item_type := rel_item_elem.get("relatedItemType"):
                related_item["relatedItemType"] = rel_item_type

            # Related item identifier
            rel_item_id_elem = rel_item_elem.xpath(
                "dc:relatedItemIdentifier", namespaces=self.NAMESPACE
            )
            if rel_item_id_elem:
                ri_elem = rel_item_id_elem[0]
                rel_item_id = {}

                if ri_elem.text:
                    rel_item_id["relatedItemIdentifier"] = ri_elem.text

                if ri_type := ri_elem.get("relatedItemIdentifierType"):
                    rel_item_id["relatedItemIdentifierType"] = ri_type

                if rel_item_id:
                    related_item["relatedItemIdentifier"] = rel_item_id

            # Creators
            creators = self._convert_related_item_creators(rel_item_elem)
            if creators:
                related_item["creators"] = creators

            # Titles
            titles = self._convert_titles_from_element(rel_item_elem)
            if titles:
                related_item["titles"] = titles

            # Publication year
            pub_year = rel_item_elem.xpath(
                "dc:publicationYear/text()", namespaces=self.NAMESPACE
            )
            if pub_year:
                related_item["publicationYear"] = pub_year[0]

            # Volume
            volume = rel_item_elem.xpath("dc:volume/text()", namespaces=self.NAMESPACE)
            if volume:
                related_item["volume"] = volume[0]

            # Issue
            issue = rel_item_elem.xpath("dc:issue/text()", namespaces=self.NAMESPACE)
            if issue:
                related_item["issue"] = issue[0]

            # Number
            number_elem = rel_item_elem.xpath("dc:number", namespaces=self.NAMESPACE)
            if number_elem:
                num_elem = number_elem[0]
                if num_elem.text:
                    related_item["number"] = num_elem.text

                if num_type := num_elem.get("numberType"):
                    related_item["numberType"] = num_type

            # First page
            first_page = rel_item_elem.xpath(
                "dc:firstPage/text()", namespaces=self.NAMESPACE
            )
            if first_page:
                related_item["firstPage"] = first_page[0]

            # Last page
            last_page = rel_item_elem.xpath(
                "dc:lastPage/text()", namespaces=self.NAMESPACE
            )
            if last_page:
                related_item["lastPage"] = last_page[0]

            # Publisher
            publisher = rel_item_elem.xpath(
                "dc:publisher/text()", namespaces=self.NAMESPACE
            )
            if publisher:
                related_item["publisher"] = publisher[0]

            # Edition
            edition = rel_item_elem.xpath(
                "dc:edition/text()", namespaces=self.NAMESPACE
            )
            if edition:
                related_item["edition"] = edition[0]

            # Contributors
            contributors = self._convert_related_item_contributors(rel_item_elem)
            if contributors:
                related_item["contributors"] = contributors

            if related_item:
                related_items.append(related_item)

        return related_items

    def _convert_related_item_creators(self, rel_item_elem: etree._Element) -> list:
        """Convert creators for related items."""
        creators = []
        creator_elements = rel_item_elem.xpath(
            "dc:creators/dc:creator", namespaces=self.NAMESPACE
        )

        for creator_elem in creator_elements:
            creator = {}

            # Name
            name_elem = creator_elem.xpath("dc:creatorName", namespaces=self.NAMESPACE)
            if name_elem:
                creator["name"] = name_elem[0].text or ""

                if name_type := name_elem[0].get("nameType"):
                    creator["nameType"] = name_type

            # Given name
            given_name = creator_elem.xpath(
                "dc:givenName/text()", namespaces=self.NAMESPACE
            )
            if given_name:
                creator["givenName"] = given_name[0]

            # Family name
            family_name = creator_elem.xpath(
                "dc:familyName/text()", namespaces=self.NAMESPACE
            )
            if family_name:
                creator["familyName"] = family_name[0]

            if creator:
                creators.append(creator)

        return creators

    def _convert_related_item_contributors(self, rel_item_elem: etree._Element) -> list:
        """Convert contributors for related items."""
        contributors = []
        contributor_elements = rel_item_elem.xpath(
            "dc:contributors/dc:contributor", namespaces=self.NAMESPACE
        )

        for contrib_elem in contributor_elements:
            contributor = {}

            # Name
            name_elem = contrib_elem.xpath(
                "dc:contributorName", namespaces=self.NAMESPACE
            )
            if name_elem:
                contributor["name"] = name_elem[0].text or ""

                if name_type := name_elem[0].get("nameType"):
                    contributor["nameType"] = name_type

            # Given name
            given_name = contrib_elem.xpath(
                "dc:givenName/text()", namespaces=self.NAMESPACE
            )
            if given_name:
                contributor["givenName"] = given_name[0]

            # Family name
            family_name = contrib_elem.xpath(
                "dc:familyName/text()", namespaces=self.NAMESPACE
            )
            if family_name:
                contributor["familyName"] = family_name[0]

            # Contributor type
            if contrib_type := contrib_elem.get("contributorType"):
                contributor["contributorType"] = contrib_type

            if contributor:
                contributors.append(contributor)

        return contributors

    def _convert_titles_from_element(self, element: etree._Element) -> list:
        """Convert titles from a given element (for related items)."""
        titles = []
        title_elements = element.xpath("dc:titles/dc:title", namespaces=self.NAMESPACE)

        for title_elem in title_elements:
            title = {}

            if title_elem.text:
                title["title"] = title_elem.text

            if title_type := title_elem.get("titleType"):
                title["titleType"] = title_type

            if lang := title_elem.get("{http://www.w3.org/XML/1998/namespace}lang"):
                title["lang"] = lang

            if title:
                titles.append(title)

        return titles

    def _convert_container(self, resource: etree._Element) -> dict | None:
        """
        Convert container information if present.
        Note: This is not a standard DataCite field but may appear in some implementations.
        """
        # Container is typically derived from relatedItems with relationType="IsPublishedIn"
        # or from series information in descriptions
        return None
