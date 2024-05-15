import React from "react";
import { i18next } from "@translations/oarepo_ui/i18next";

export const ResultsPerPageLabel = (cmp) => (
  <div className="results-per-page">
    <span>{i18next.t("resultsPerPage")}:</span> {cmp}
  </div>
);
