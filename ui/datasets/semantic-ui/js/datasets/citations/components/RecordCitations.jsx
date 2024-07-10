import React, { lazy, Suspense } from "react";
import PropTypes from "prop-types";

import { i18next } from "@translations/i18next";
import { Loader, Segment } from "semantic-ui-react";

const CitationField = lazy(() => import("./CitationField"));

export const RecordCitations = ({ record, citationStyles, defaultStyle }) => {
  return (
    <Suspense
      fallback={
        <Segment basic placeholder className="transparent">
          <Loader active size="medium">{i18next.t("Loading")}…</Loader>
        </Segment>
      }
    >
      <CitationField record={record} styles={citationStyles} defaultStyle={defaultStyle} />
    </Suspense>
  );
};

RecordCitations.propTypes = {
  record: PropTypes.object.isRequired,
};
