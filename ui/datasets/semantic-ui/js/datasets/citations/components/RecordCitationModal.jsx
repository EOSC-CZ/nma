import React, { lazy, Suspense } from "react";
import PropTypes from "prop-types";

import { i18next } from "@translations/i18next";
import { Dimmer, Loader, Segment } from "semantic-ui-react";

const CitationList = lazy(() => import("./CitationList"));

export const RecordCitationModal = ({ record }) => {
  return (
    <Suspense
      fallback={
        <Dimmer.Dimmable as={Segment} className="borderless" basic placeholder dimmed role="presentation">
          <Dimmer simple inverted>
            <Loader size="medium">{i18next.t("Loading")}…</Loader>
          </Dimmer>
        </Dimmer.Dimmable>
      }
    >
      <CitationList record={record} />
    </Suspense>
  );
};

RecordCitationModal.propTypes = {
  record: PropTypes.object.isRequired,
};
