import React, { useContext } from "react";
import PropTypes from "prop-types";
import { i18next } from "@translations/oarepo_ui/i18next";
import { withState, buildUID as searchkitUID } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";

const CountElement = ({ totalResults }) => {
  return (
    <div>
      <label className="rel-mr-1">
        {i18next.t("totalResults", { count: totalResults })}
      </label>
    </div>
  );
};

const ResultCount = ({ currentResultsState = {} }) => {
  const total = currentResultsState?.data?.total;
  const { loading } = currentResultsState;
  // determine if we are in searchApp context or pure searchkit
  const searchAppContext = useContext(SearchConfigurationContext);
  let buildUID = searchkitUID;
  if (searchAppContext === true) buildUID = searchAppContext.buildUID;
  const resultsLoaded = !loading && total > 0;

  return (
    resultsLoaded && (
      <CountElement totalResults={total} />
    )
  );
};

CountElement.propTypes = {
  totalResults: PropTypes.number.isRequired,
};

ResultCount.propTypes = {
  currentResultsState: PropTypes.object,
};

export const ResultCountWithState = withState(ResultCount);
