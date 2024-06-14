import React, { lazy, Suspense } from "react";
import PropTypes from "prop-types";

import { i18next } from "@translations/i18next";
import { Loader, Segment } from "semantic-ui-react";

const CitationList = lazy(() => import("./CitationList"));

export const RecordCitations = ({ record }) => {
  return (
    <Suspense
      fallback={
        <Segment basic placeholder className="transparent">
          <Loader active size="medium">{i18next.t("Loading")}…</Loader>
        </Segment>
      }
    >
      <CitationList record={record} />
    </Suspense>
  );
};

RecordCitations.propTypes = {
  record: PropTypes.object.isRequired,
};
