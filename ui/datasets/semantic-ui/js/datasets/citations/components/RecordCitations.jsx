import React, { lazy, Suspense } from "react";
import PropTypes from "prop-types";

import { i18next } from "@translations/i18next";
import { Loader, Segment } from "semantic-ui-react";

const CitationField = lazy(() => import("./CitationField"));

const CITATION_STYLES = [
  { style: "apa", label: "APA" },
  { style: "harvard-cite-them-right", label: "Harvard" },
  { style: "modern-language-association", label: "MLA" },
  { style: "vancouver", label: "Vancouver" },
  { style: "chicago-fullnote-bibliography", label: "Chicago" },
  { style: "ieee", label: "IEEE" },
];

const DEFAULT_STYLE = "apa";

export const RecordCitations = ({ record }) => {
  return (
    <Suspense
      fallback={
        <Segment basic placeholder className="transparent">
          <Loader active size="medium">{i18next.t("Loading")}…</Loader>
        </Segment>
      }
    >
      <CitationField record={record} styles={CITATION_STYLES} defaultStyle={DEFAULT_STYLE} />
    </Suspense>
  );
};

RecordCitations.propTypes = {
  record: PropTypes.object.isRequired,
};
