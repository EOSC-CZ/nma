"""OAI writer preserving manually edited dataset records."""

from __future__ import annotations

import copy

from oarepo_oaipmh_harvester.writers import OAIServiceWriter


class CollisionAwareWriter(OAIServiceWriter):
    """Do not replace manually edited records with harvested metadata."""

    def add_oai_related_identifier(
            self,
            record,
            oai_identifier,
    ):
        """Add the OAI identifier without changing other metadata."""
        metadata = record.setdefault("metadata", {})
        related_identifiers = metadata.setdefault("related_identifiers", [])

        for related_identifier in related_identifiers:
            identifier = related_identifier.get("identifier")
            scheme = related_identifier.get("scheme")

            if identifier == oai_identifier and scheme == "other":
                return #already there

        related_identifiers.append(
            {
                "identifier": oai_identifier,
                "scheme": "other",
                "relation_type": {
                    "id": "IsIdenticalTo", #todo ok id?
                },
            }
        )

    def _save_and_publish_record(
            self,
            transformed_data,
            pid_value,
            op_type,
            stream_entry,
            oai_identifier,
    ) :
        """Preserve manual metadata and delegate saving to the base writer."""
        final_data = transformed_data
        final_op_type = op_type


        if pid_value and op_type in {"update", "delete"}: #the two only possible actions
            current_record = self.service.read(
                self._identity,
                pid_value,
            )

            current_data = copy.deepcopy(current_record.data)

            manually_edited = False
            editors = current_data.get("editors", [])

            for editor in editors:
                last_edited = editor.get("last_edited")

                if last_edited:
                    manually_edited = True
                    break

            if manually_edited:

                self.add_oai_related_identifier(
                    current_data,
                    oai_identifier,
                )

                final_data = current_data

                final_op_type = "update" #todo: we will ignore deleting, ok?

        return super()._save_and_publish_record(
            final_data,
            pid_value,
            final_op_type,
            stream_entry,
            oai_identifier,
        )
