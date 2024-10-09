# Add support for DCAT-AP serialization (both "export" on UI page and content negotiation in API) 
# 
# Try to validate harvested records in nma against https://github.com/inveniosoftware/datacite/blob/master/datacite/schemas/datacite-v4.3.json
# 
# Compare metadata schema of nma (datacite 4.5 based) with schema4.3 in examples at https://github.com/inveniosoftware/datacite/blob/master/tests/data/4.3/
# 
# Create marshmallow schema that will convert nma to 4.3 compatible json and write tests
# 
# Extend DCAT serializer, replace DCAT schema with our - see https://github.com/inveniosoftware/invenio-rdm-records/tree/master/invenio_rdm_records/resources/serializers/dcat + tests
# 
# Register the serializer to UI exports
# Write API connector for content negotiation


import json
import argparse

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_json_keys(json1, json2):
    keys1 = set(json1.keys())
    keys2 = set(json2.keys())

    only_in_json1 = keys1 - keys2
    only_in_json2 = keys2 - keys1

    # Recursively check for matching keys
    matching_keys = keys1 & keys2
    recursive_diff = {}

    for key in matching_keys:
        if isinstance(json1[key], dict) and isinstance(json2[key], dict):
            # Recursively compare nested dictionaries
            only_in_nested1, only_in_nested2, nested_diff = compare_json_keys(json1[key], json2[key])
            if only_in_nested1 or only_in_nested2 or nested_diff:
                recursive_diff[key] = {
                    'only_in_json1': only_in_nested1,
                    'only_in_json2': only_in_nested2,
                    'nested_diff': nested_diff
                }

    return only_in_json1, only_in_json2, recursive_diff

def sort_json_keys(data):
    """Recursively sort JSON object keys."""
    if isinstance(data, dict):
        # Sort the dictionary by keys
        return {key: sort_json_keys(value) for key in sorted(data) for value in [data[key]]}
    elif isinstance(data, list):
        # Keep the list as is
        return data
    else:
        # Return the data as is if it's neither a dict nor a list
        return data

def sort_json_file(input_file, output_file):
    """Load a JSON file, sort its keys, and write to a new file."""
    with open(input_file, 'r') as f:
        data = json.load(f)

    sorted_data = sort_json_keys(data)

    with open(output_file, 'w') as f:
        json.dump(sorted_data, f, indent=4)

def main(file1, file2):
    json1 = load_json(file1)
    json2 = load_json(file2)
    
    # Sort the JSON keys before comparing
    sorted_json1 = sort_json_keys(json1)
    sorted_json2 = sort_json_keys(json2)

    only_in_json1, only_in_json2, recursive_diff = compare_json_keys(sorted_json1, sorted_json2)

    print(f"Keys only in {file1}: {only_in_json1}")
    print(f"Keys only in {file2}: {only_in_json2}")

    if recursive_diff:
        print("Differences in matching keys:")
        for key, diff in recursive_diff.items():
            print(f"Key: {key}")
            print(f"  Only in {file1}: {diff['only_in_json1']}")
            print(f"  Only in {file2}: {diff['only_in_json2']}")
            if 'nested_diff' in diff and diff['nested_diff']:
                print(f"  Nested differences: {diff['nested_diff']}")
    else:
        print("No differences in matching keys.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare JSON keys between two files.")
    parser.add_argument('file1', type=str, help='Path to the first JSON file')
    parser.add_argument('file2', type=str, help='Path to the second JSON file')

    args = parser.parse_args()
    main(args.file1, args.file2)
