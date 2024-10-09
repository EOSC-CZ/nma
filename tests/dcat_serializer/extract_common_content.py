import json
import argparse

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_common_content(json1, json2):
    common_content = {}

    # Find common keys
    keys1 = set(json1.keys())
    keys2 = set(json2.keys())
    matching_keys = keys1 & keys2

    for key in matching_keys:
        if isinstance(json1[key], dict) and isinstance(json2[key], dict):
            nested_common = extract_common_content(json1[key], json2[key])
            # include only if common
            if nested_common:  
                common_content[key] = nested_common
        else:
            # if -eq, include in common content
            if json1[key] == json2[key]:
                common_content[key] = json1[key]

    return common_content

def main(file1, file2, output_file):
    json1 = load_json(file1)
    json2 = load_json(file2)

    common_content = extract_common_content(json1, json2)

    with open(output_file, 'w') as outfile:
        json.dump(common_content, outfile, indent=2)

    print(f"Common content saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract common content between two JSON files.")
    parser.add_argument('file1', type=str, help='Path to the first JSON file')
    parser.add_argument('file2', type=str, help='Path to the second JSON file')
    parser.add_argument('output_file', type=str, help='Path to the output JSON file')

    args = parser.parse_args()
    main(args.file1, args.file2, args.output_file)
