import React from "react";
import { i18next } from "@translations/oarepo_ui/i18next";

export const ResultsPerPageLabel = (cmp) => (
  <span className="grey rel-mr-2">
    <span className="rel-mr-1">{i18next.t("resultsPerPage")}:</span> {cmp}
  </span>
);
