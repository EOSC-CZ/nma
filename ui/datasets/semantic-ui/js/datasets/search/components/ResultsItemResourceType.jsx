import React from "react";
import { SearchFacetLink } from "./SearchFacetLink";
import { i18next } from "@translations/i18next";
import PropTypes from "prop-types";

export const ResultsItemResourceType = ({
  resourceType = {},
  searchUrl = "/",
}) => (
  <SearchFacetLink
    searchUrl={searchUrl}
    searchFacet="metadata_types_resourceTypeGeneral"
    value={resourceType.resourceTypeGeneral}
    title={`${i18next.t("Find all records")} ${i18next.t(
      "by this dataset type"
    )}`}
    label={resourceType.resourceTypeGeneral || "No resource type"}
    className="resource-type-link"
  />
);

ResultsItemResourceType.propTypes = {
  resourceType: PropTypes.object,
  searchUrl: PropTypes.string,
};
