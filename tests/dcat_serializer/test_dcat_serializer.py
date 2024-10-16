import json
import jsonschema
from common.datasets.serializers.dcat import DCATAPSerializer

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def validate_json(json_data, schema_data):
    jsonschema.validate(json_data, schema_data)

def normalize_json(json_data):
    """Consistent JSON formatting for comparison."""
    return json.dumps(json_data, indent=2, sort_keys=True)

def test_dcatap_serializer():
    input_file = './input_file.json'
    expected_output_file = './expected_output_file.json'
    
    json_data = load_json(input_file)
    expected_output_data = load_json(expected_output_file)
    
    serializer = DCATAPSerializer()
    output_data = serializer.serialize_object(json_data)
    
    # dict
    if isinstance(output_data, str):
        output_data = json.loads(output_data)
    
    output_data_str = normalize_json(output_data)
    expected_output_data_str = normalize_json(expected_output_data)
    
    assert output_data_str == expected_output_data_str
    return output_data

def test_dcatap_schema_validation():
    output_data = test_dcatap_serializer()
    schema_file = './datacite-4.3.json'
    
    schema_data = load_json(schema_file)
    
    metadata = output_data.get('metadata', {})
    
    assert validate_json(metadata, schema_data) is None
    

if __name__ == "__main__":
    test_dcatap_schema_validation()