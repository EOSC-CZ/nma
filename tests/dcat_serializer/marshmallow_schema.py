import json
from marshmallow import Schema, fields, validate, ValidationError

# nametype?
# schemeUri
class NameIdentifierSchema(Schema):
    nameIdentifier = fields.String(required=True)
    nameIdentifierScheme = fields.String(required=True)

class AffiliationSchema(Schema):
    name = fields.String(required=True)

class CreatorSchema(Schema):
    name = fields.String(required=True)
    nameType = fields.String(required=True, validate=validate.OneOf(["Organizational", "Personal"]))
    givenName = fields.String()
    familyName = fields.String()
    nameIdentifiers = fields.List(fields.Nested(NameIdentifierSchema))
    affiliation = fields.List(fields.Nested(AffiliationSchema))
    lang = fields.String()

class TitleSchema(Schema):
    title = fields.String(required=True)
    titleType = fields.String(validate=validate.OneOf(["AlternativeTitle", "Subtitle", "TranslatedTitle", "Other"]))

class FundingReferenceSchema(Schema):
    funderName = fields.String(required=True)
    funderIdentifier = fields.String()
    funderIdentifierType = fields.String(validate=validate.OneOf(["ISNI", "GRID", "Crossref Funder ID", "ROR", "Other"]))
    awardNumber = fields.String()
    awardUri = fields.String()
    awardTitle = fields.String()

class DateSchema(Schema):
    date = fields.String(required=True)
    dateType = fields.String(validate=validate.OneOf([
        "Accepted", "Available", "Copyrighted", "Collected", "Created", "Issued", "Submitted", "Updated", "Valid", "Withdrawn", "Other"
    ]))

class RightsSchema(Schema):
    rights = fields.String(required=True)
    rightsUri = fields.String()
    rightsIdentifier = fields.String()
    rightsIdentifierScheme = fields.String()
    schemeUri = fields.String()

class RelatedIdentifierSchema(Schema):
    relatedIdentifier = fields.String(required=True)
    relatedIdentifierType = fields.String(required=True)
    relationType = fields.String(required=True)

class DataCiteSchema(Schema):
    identifiers = fields.List(fields.Nested(RelatedIdentifierSchema), required=True)
    creators = fields.List(fields.Nested(CreatorSchema), required=True)
    titles = fields.List(fields.Nested(TitleSchema), required=True)
    publisher = fields.String(required=True)
    publicationYear = fields.String(required=True)
    types = fields.Dict(required=True)
    schemaVersion = fields.String(const="http://datacite.org/schema/kernel-4", required=True)
    fundingReferences = fields.List(fields.Nested(FundingReferenceSchema))
    dates = fields.List(fields.Nested(DateSchema))
    rightsList = fields.List(fields.Nested(RightsSchema))

def convert_data(input_data):
    metadata = input_data.get("metadata", {})

    creators = [
        {
            "name": creator.get("name"),
            "nameType": creator.get("nameType", "Personal"),  # Default to "Personal" if missing
            "givenName": creator.get("givenName", ""),  # Default to empty string
            "familyName": creator.get("familyName", ""),  # Default to empty string
            "nameIdentifiers": creator.get("nameIdentifiers", []),
            "affiliation": [{"name": aff["name"]} for aff in creator.get("affiliation", [])],
        }
        for creator in metadata.get("creators", [])
    ]

    titles = [
        {
            "title": title.get("title", ""),  # empty
            "titleType": title.get("titleType", "Other"),  # other?
        }
        for title in metadata.get("titles", [])
    ]

    funding_references = [
        {
            "funderName": fund["funderName"],
            "funderIdentifier": fund.get("funderIdentifier"),
            "funderIdentifierType": fund.get("funderIdentifierType"),
            "awardNumber": fund.get("awardNumber"),
            "awardUri": fund.get("awardURI"),
            "awardTitle": fund.get("awardTitle"),
        }
        for fund in metadata.get("fundingReferences", [])
    ]

    dates = [
        {
            "date": date.get("date"),
            "dateType": date.get("dateType"),
        }
        for date in metadata.get("dates", [])
    ]

    rights_list = [
        {
            "rights": right.get("rights"),
            "rightsUri": right.get("rightsURI"),
            "rightsIdentifier": right.get("rightsIdentifier"),
            "rightsIdentifierScheme": right.get("rightsIdentifierScheme"),
            "schemeUri": right.get("schemeUri"), #?
        }
        for right in metadata.get("rightsList", [])
    ]

    return {
        "identifiers": [{"relatedIdentifier": input_data.get("id"), "relatedIdentifierType": "DOI", "relationType": "IsIdentifiedBy"}], 
        "creators": creators,
        "titles": titles,
        "publisher": metadata.get("publisher", {}).get("name", "Unknown Publisher"),
        "publicationYear": metadata.get("publicationYear", "Unknown Year"),
        "types": {
            "resourceType": metadata.get("types", [{}])[0].get("resourceType", "Dataset"),
            "resourceTypeGeneral": metadata.get("types", [{}])[0].get("resourceTypeGeneral", "Dataset"),
        },
        "schemaVersion": "http://datacite.org/schema/kernel-4",
        "fundingReferences": funding_references,
        "dates": dates,
        "rightsList": rights_list,
    }

def main():
    input_file = "ours.json"
    
    with open(input_file, 'r') as f:
        input_data = json.load(f)

    data_cite_data = convert_data(input_data)

    # Validate 
    schema = DataCiteSchema()
    try:
        result = schema.load(data_cite_data)
        print("Validation successful:", result)

        # Save to new JSON
        output_file = f"{input_file.split('.')[0]}_converted.json"
        with open(output_file, 'w') as out_f:
            json.dump(result, out_f, indent=4)
        print(f"Converted data saved to {output_file}")

    except ValidationError as err:
        print("Validation errors:", err.messages)

if __name__ == "__main__":
    main()
