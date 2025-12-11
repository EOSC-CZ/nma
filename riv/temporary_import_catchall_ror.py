#!/usr/bin/env python3
"""
Extract ROR identifiers and affiliation names from transformed JSON files
and enrich them with data from the ROR API.

The script:
1. Scans all data/*_transformed.json files
2. Extracts unique affiliations (by ROR ID and name)
3. Queries the ROR API for each affiliation
4. Outputs a YAML file with enriched affiliation data
"""

import json
import time
from pathlib import Path
from typing import Dict, Set, Tuple

import requests
import yaml
from invenio_access.permissions import system_identity
from invenio_pidstore.errors import PIDAlreadyExists
from invenio_records_resources.proxies import current_service_registry


class RORImporter:
    """Import and enrich affiliation data from ROR API."""

    ROR_API_BASE = "https://api.ror.org/organizations"

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.affiliations: Dict[str, Dict] = {}  # key: ror_id, value: affiliation data

    def extract_affiliations(self) -> Set[Tuple[str, str]]:
        """
        Extract unique affiliations from all transformed JSON files.

        Extracts ROR IDs from:
        - creators/affiliations
        - contributors/affiliations
        - funding/funder
        - any other location with ROR identifiers

        Returns:
            Set of tuples (ror_id, name)
        """
        affiliations = set()

        # Find all transformed JSON files
        json_files = sorted(self.data_dir.glob("*_transformed.json"))
        print(f"Found {len(json_files)} transformed JSON files")

        for json_file in json_files:
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                metadata = data.get("metadata", {})

                # Extract affiliations from creators
                creators = metadata.get("creators", [])
                for creator in creators:
                    creator_affiliations = creator.get("affiliations", [])
                    for affiliation in creator_affiliations:
                        ror_id = affiliation.get("id")
                        name = affiliation.get("name")
                        if ror_id and name:
                            affiliations.add((ror_id, name))

                # Extract affiliations from contributors if they exist
                contributors = metadata.get("contributors", [])
                for contributor in contributors:
                    contributor_affiliations = contributor.get("affiliations", [])
                    for affiliation in contributor_affiliations:
                        ror_id = affiliation.get("id")
                        name = affiliation.get("name")
                        if ror_id and name:
                            affiliations.add((ror_id, name))

                # Extract ROR IDs from funding/funder
                funding = metadata.get("funding", [])
                for funding_entry in funding:
                    funder = funding_entry.get("funder", {})
                    ror_id = funder.get("id")
                    name = funder.get("name")
                    if ror_id and name:
                        affiliations.add((ror_id, name))

            except Exception as e:
                print(f"Error processing {json_file}: {e}")
                continue

        print(f"Extracted {len(affiliations)} unique affiliations")
        return affiliations

    def fetch_ror_data(self, ror_id: str) -> Dict:
        """
        Fetch affiliation data from ROR API.

        Args:
            ror_id: ROR identifier (without https://ror.org/ prefix)

        Returns:
            Dictionary with ROR data
        """
        url = f"{self.ROR_API_BASE}/{ror_id}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching ROR data for {ror_id}: {e}")
            return {}

    def transform_ror_data(self, ror_data: Dict, original_name: str) -> Dict:
        """
        Transform ROR API response to the desired output format.

        Args:
            ror_data: Raw data from ROR API
            original_name: Original affiliation name from the dataset

        Returns:
            Transformed dictionary
        """
        result = {
            "id": ror_data.get("id", "").replace("https://ror.org/", ""),
            "name": ror_data.get("name", original_name),
            "status": ror_data.get("status", "unknown"),
        }

        # Extract acronyms and titles from names
        names = ror_data.get("names", [])
        acronyms = []
        titles = {}

        for name_entry in names:
            types = name_entry.get("types", [])
            lang = name_entry.get("lang")
            value = name_entry.get("value")

            if "acronym" in types and value:
                acronyms.append(value)
            elif "label" in types and lang and value:
                titles[lang] = value

        # Add first acronym if available
        if acronyms:
            result["acronym"] = acronyms[0]

        # Extract country information
        addresses = ror_data.get("addresses", [])
        if addresses:
            address = addresses[0]
            result["country"] = address.get("country_geonames_id")
            # Try to get country code from locations

        # Better country extraction
        locations = ror_data.get("locations", [])
        if locations:
            geonames = locations[0].get("geonames_details", {})
            result["country"] = geonames.get("country_code")
            result["country_name"] = geonames.get("country_name")
            result["location_name"] = geonames.get("name")

        # Extract identifiers
        identifiers = []

        # Add ROR identifier
        ror_id = result["id"]
        if ror_id:
            identifiers.append({"identifier": ror_id, "scheme": "ROR"})

        # Add external identifiers (it's a list in ROR API v2)
        external_ids = ror_data.get("external_ids", [])

        for ext_id in external_ids:
            id_type = ext_id.get("type", "").lower()
            preferred = ext_id.get("preferred")
            all_ids = ext_id.get("all", [])

            if id_type == "grid" and preferred:
                identifiers.append({"identifier": preferred, "scheme": "grid"})
            elif id_type == "isni" and all_ids:
                for isni_id in all_ids:
                    identifiers.append({"identifier": isni_id, "scheme": "isni"})
            elif id_type == "wikidata" and all_ids:
                # Use first one or preferred
                wikidata_id = preferred if preferred else all_ids[0]
                identifiers.append({"identifier": wikidata_id, "scheme": "wikidata"})
            elif id_type == "fundref" and all_ids:
                # Use first one or preferred
                fundref_id = preferred if preferred else all_ids[0]
                identifiers.append({"identifier": fundref_id, "scheme": "fundref"})

        # do not store identifiers for now
        # if identifiers:
        #     result["identifiers"] = identifiers

        # Add titles if available
        if titles:
            result["title"] = titles

        # Extract types
        types = ror_data.get("types", [])
        if types:
            result["types"] = types

        return result

    def process_affiliations(self, affiliations: Set[Tuple[str, str]]):
        """
        Process all affiliations by fetching ROR data and transforming it.

        Args:
            affiliations: Set of tuples (ror_id, name)
        """
        total = len(affiliations)
        for idx, (ror_id, name) in enumerate(sorted(affiliations), 1):
            print(f"Processing {idx}/{total}: {ror_id} - {name}")

            # Check if already processed
            if ror_id in self.affiliations:
                print("  Already processed, skipping...")
                continue

            # Fetch data from ROR API
            ror_data = self.fetch_ror_data(ror_id)

            if ror_data:
                # Transform and store
                transformed = self.transform_ror_data(ror_data, name)
                self.affiliations[ror_id] = transformed
                print("  ✓ Successfully processed")
            else:
                # Store minimal data if API call failed
                self.affiliations[ror_id] = {
                    "id": ror_id,
                    "name": name,
                    "status": "unknown",
                }
                print("  ✗ Failed to fetch ROR data, using minimal info")

            # Be nice to the API - add a small delay
            if idx < total:
                time.sleep(0.5)

    def save_affiliations(self):
        """Save the processed affiliations to both affiliations and funders services."""
        # Get both services
        affiliation_service = current_service_registry.get("affiliations")
        funder_service = current_service_registry.get("funders")

        for idx, aff in enumerate(self.affiliations.values(), 1):
            print(f"Saving {idx}/{len(self.affiliations)} - {aff.get('name')}")

            # Save to affiliations service
            try:
                affiliation_service.create(system_identity, aff)
                print("  ✓ Saved to affiliations")
            except PIDAlreadyExists:
                print("  - Already exists in affiliations")
            except Exception as e:
                print(f"  ✗ Error saving to affiliations: {e}")
                import traceback

                traceback.print_exc()

            # Save to funders service (same data structure is compatible)
            try:
                funder_service.create(system_identity, aff)
                print("  ✓ Saved to funders")
            except PIDAlreadyExists:
                print("  - Already exists in funders")
            except Exception as e:
                print(f"  ✗ Error saving to funders: {e}")
                import traceback

                traceback.print_exc()

        # output as yaml array
        with open("ror_affiliations_imported.yaml", "w", encoding="utf-8") as f:
            yaml.dump(
                sorted(self.affiliations.values(), key=lambda x: x.get("name", "")),
                f,
                allow_unicode=True,
                sort_keys=True,
            )

    def run(self):
        """Run the complete import process."""
        print("=" * 70)
        print("ROR Affiliation Importer")
        print("=" * 70)
        print()

        # Step 1: Extract affiliations
        print("Step 1: Extracting affiliations from JSON files...")
        affiliations = self.extract_affiliations()
        print()

        # Step 2: Process affiliations
        print("Step 2: Fetching and processing ROR data...")
        self.process_affiliations(affiliations)
        print()

        # Step 3: Save to YAML
        print("Step 3: Saving results...")
        self.save_affiliations()
        print()

        print("=" * 70)
        print("Import complete!")
        print("=" * 70)
