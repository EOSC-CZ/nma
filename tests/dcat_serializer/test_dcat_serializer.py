# Add support for DCAT-AP serialization (both "export" on UI page and content negotiation in API) 
# 
# Try to validate harvested records in nma against https://github.com/inveniosoftware/datacite/blob/master/datacite/schemas/datacite-v4.3.json
# 
# Compare metadata schema of nma (datacite 4.5 based) with schema4.3 in examples at https://github.com/inveniosoftware/datacite/blob/master/tests/data/4.3/

# UPDATE: SKIP THIS (no marshmallow)
# Create marshmallow schema that will convert nma to 4.3 compatible json and write tests


# Extend DCAT serializer, replace DCAT schema with our - see https://github.com/inveniosoftware/invenio-rdm-records/tree/master/invenio_rdm_records/resources/serializers/dcat + tests
# 
# Register the serializer to UI exports
# Write API connector for content negotiation

import jsonschema
import json
import argparse

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# now use jsonschema to validate the JSON file against the schema
def validate_json(json_file, schema_file):
    json_data = load_json(json_file)
    schema_data = load_json(schema_file)
    jsonschema.validate(json_data, schema_data)

def main(json_file, schema_file):
    validate_json(json_file, schema_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a JSON file against a schema.")
    parser.add_argument("json_file", help="Path to the JSON file.")
    parser.add_argument("schema_file", help="Path to the schema file.")
    args = parser.parse_args()
    main(args.json_file, args.schema_file)