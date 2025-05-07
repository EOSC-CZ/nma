import yaml


def capitalize(s):
    return s[0].upper() + s[1:] if s else s


def merge_relation_types(orig_file, added_md, target_file):
    with open(orig_file) as f:
        orig_data = list(yaml.safe_load_all(f))
    with open(added_md) as f:
        added_data = yaml.safe_load(f)

    for entry in orig_data:
        entry["id"] = capitalize(entry["id"])
        if "props" in entry:
            entry["props"]["pair"] = capitalize(entry["props"]["pair"])

    orig_data_by_id = {item["id"]: item for item in orig_data}
    added_data_by_id = {item["id"]: item for item in added_data}

    for key, value in added_data_by_id.items():
        if key in orig_data_by_id:
            orig_props = orig_data_by_id[key].setdefault("props", {})
            for prop_key, prop_value in value["props"].items():
                if prop_key not in orig_props:
                    orig_props[prop_key] = prop_value
        else:
            orig_data_by_id[key] = value

    orig_data = orig_data_by_id.values()
    with open(target_file, "w") as f:
        yaml.safe_dump_all(orig_data, f, sort_keys=True, allow_unicode=True)


if __name__ == "__main__":
    orig_file = "fixtures/relation-types.yaml"
    added_md = "fixtures/relation-types-4.6.yaml"
    target_file = "fixtures/merged_relation_types.yaml"

    merge_relation_types(orig_file, added_md, target_file)
