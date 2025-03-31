import React, { useContext } from "react";
import { Sort, ResultsPerPage } from "react-searchkit";
import { Grid } from "semantic-ui-react";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";
import { i18next } from "@translations/i18next";
import PropTypes from "prop-types";

const ResultsPerPageLabel = (cmp) => (
  <>
    <span className="rel-mr-1">{i18next.t("Results per page:")}</span> {cmp}
  </>
);

const SortLabel = (cmp) => (
  <>
    <span className="rel-mr-1">{i18next.t("Sort:")}</span> {cmp}
  </>
);

const ResultsPerPageLabelMobile = (cmp) => cmp;

const SortLabelMobile = (cmp) => cmp;

export const ResultOptions = ({ currentResultsState = {} }) => {
  const { total } = currentResultsState.data;
  const { sortOptions, paginationOptions, sortOrderDisabled } = useContext(
    SearchConfigurationContext
  );
  return (
    <React.Fragment>
      {(total || null) && (
        <>
          <Grid.Column textAlign="left" width={3}>
            <p>{i18next.t("Results: {{count}}", { count: total })}</p>
          </Grid.Column>
          <Grid.Column
            textAlign="right"
            width={13}
            floated="right"
            className="computer tablet only"
          >
            {sortOptions && (
              <Sort
                sortOrderDisabled={sortOrderDisabled || false}
                values={sortOptions}
                ariaLabel={i18next.t("Sort")}
                label={SortLabel}
              />
            )}
            <span className="rel-mr-1" />
            <ResultsPerPage
              values={paginationOptions.resultsPerPage}
              label={ResultsPerPageLabel}
            />
          </Grid.Column>
          <Grid.Column
            textAlign="right"
            width={13}
            floated="right"
            className="mobile only"
          >
            {sortOptions && (
              <Sort
                sortOrderDisabled={sortOrderDisabled || false}
                values={sortOptions}
                ariaLabel={i18next.t("Sort")}
                label={SortLabelMobile}
              />
            )}
            <span className="rel-mr-1" />
            <ResultsPerPage
              values={paginationOptions.resultsPerPage}
              label={ResultsPerPageLabelMobile}
            />
          </Grid.Column>
        </>
      )}
    </React.Fragment>
  );
};

PropTypes.ResultOptions = {
  currentResultsState: PropTypes.object,
};
