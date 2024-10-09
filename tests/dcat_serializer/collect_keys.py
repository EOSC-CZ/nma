import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def collect_keys(data, keys_set):
    if isinstance(data, dict):
        for key in data.keys():
            keys_set.add(key)
            collect_keys(data[key], keys_set)
    elif isinstance(data, list):
        for item in data:
            collect_keys(item, keys_set)

keys_1 = set()
keys_2 = set()
json1 = load_json("./datacite-4.3.json")
json2 = load_json("./datasets-1.0.0.json")

collect_keys(json1, keys_1)
collect_keys(json2, keys_2)

only_in_1 = keys_1 - keys_2
only_in_2 = keys_2 - keys_1

common_keys = keys_1 & keys_2 

print("Keys only in Datacite-4.3:")
print(only_in_1)
print("\nKeys only in Datasets-1.0.0:")
print(only_in_2)
print("\nCommon keys:")
print(common_keys)
