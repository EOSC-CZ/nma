#!/bin/bash

#
# ----------------- WARNING -----------------
# The script wont work if class DatasetsPermissionPolicyMixin does not have can_publish = [AnyUser()] permission
# 
#------------------ WARNING ------------------
#

# Create user and token
token=$(./run.sh invenio tokens create -n demo-data -u demo@test.com)

# Dates
today=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
expired1=$(date -u -d "-3 days" +"%Y-%m-%dT%H:%M:%SZ")
expired2=$(date -u -d "-5 days" +"%Y-%m-%dT%H:%M:%SZ")
fresh=$(date -u -d "-1 days" +"%Y-%m-%dT%H:%M:%SZ")

# Record 1: expired last_checked
metadata_json_1='{
  "metadata": {
    "creators": [
      {
        "person_or_org": {
          "family_name": "Smith",
          "given_name": "John",
          "name": "Smith, John",
          "type": "personal"
        }
      }
    ],
    "publication_date": "2025",
    "resource_type": {
      "id": "dataset"
    },
    "title": "Test Record that needs checking",
    "persistent_url": "https://doi.org/10.5281/zenodo.17801799",
    "last_checked": "'"$expired1"'"
  },
  "files": {"enabled": false}
}'



# Record 2: never checked (no last_checked)
metadata_json_2='{
  "metadata": {
    "creators": [
      {
        "person_or_org": {
          "family_name": "Nguyen",
          "given_name": "Hien",
          "name": "Nguyen, Hien",
          "type": "personal"
        }
      },
      {
        "person_or_org": {
          "family_name": "Kumar",
          "given_name": "Asha",
          "name": "Kumar, Asha",
          "type": "personal"
        }
      }
    ],
    "publication_date": "2025",
    "resource_type": {
      "id": "dataset"
    },
    "title": "Test Record never checked",
    "persistent_url": "https://doi.org/10.5281/zenodo.17801800"
  },
  "files": {"enabled": false}
}'


metadata_json_3='{
  "metadata": {
    "creators": [
      {"person_or_org": {"family_name": "Johnson","given_name": "Emily","name": "Johnson, Emily","type": "personal"}},
      {"person_or_org": {"family_name": "Nguyen","given_name": "Hien","name": "Nguyen, Hien","type": "personal"}}
    ],
    "publication_date": "2025",
    "resource_type": {"id": "dataset"},
    "title": "Fresh Record – Coastal Marine Species",
    "persistent_url": "https://doi.org/10.5281/zenodo.17801801",
    "last_checked": "'"$fresh"'"
  },
  "files": {"enabled": false}
}'


metadata_json_4='{
  "metadata": {
    "creators": [
      {"person_or_org": {"family_name": "Martinez","given_name": "Laura","name": "Martinez, Laura","type": "personal"}},
      {"person_or_org": {"family_name": "Kumar","given_name": "Asha","name": "Kumar, Asha","type": "personal"}}
    ],
    "publication_date": "2025",
    "resource_type": {"id": "dataset"},
    "title": "Never Checked Record 1 – Forest Biodiversity",
    "persistent_url": "https://doi.org/10.5281/zenodo.17801802"
  },
  "files": {"enabled": false}
}'

# Function to create and publish dataset
publish_dataset() {
    local metadata_json="$1"
    response=$(curl -s -k -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $token" \
      -d "$metadata_json" \
      https://127.0.0.1:5000/api/datasets)

    publish_link=$(echo "$response" | jq -r '.links.publish')
    curl -k -X POST -H "Authorization: Bearer $token" "$publish_link"

    title=$(echo "$metadata_json" | jq -r '.metadata.title')
    echo "Published dataset: $title"
    echo "Publish link: $publish_link"
}

# Publish both datasets
publish_dataset "$metadata_json_1"
publish_dataset "$metadata_json_2"
publish_dataset "$metadata_json_3"
publish_dataset "$metadata_json_4"
