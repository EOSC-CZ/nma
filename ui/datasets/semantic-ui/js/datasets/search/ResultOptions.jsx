import Overridable from "react-overridable";
import React, { useContext } from "react";
import {
  Count,
  LayoutSwitcher,
  ResultsMultiLayout,
  Sort,
  ResultsList,
  ResultsGrid,
  ResultsPerPage,
} from "react-searchkit";
import { Grid } from "semantic-ui-react";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";
import { i18next } from "@translations/i18next";
import { AppMedia } from "@js/invenio_theme/Media";

export const ResultsPerPageLabel = (cmp) => (
  <>
    <span className="rel-mr-1">{i18next.t("Results per page:")}</span> {cmp}
  </>
);

export const SortLabel = (cmp) => (
  <>
    <span className="rel-mr-1">{i18next.t("Sort:")}</span> {cmp}
  </>
);

export const ResultOptions = ({ currentResultsState = {} }) => {
  const { MediaContextProvider, Media } = AppMedia;
  const { total } = currentResultsState.data;
  const {
    sortOptions,
    paginationOptions,
    sortOrderDisabled,
    layoutOptions,
    buildUID,
    resultsPerPage,
  } = useContext(SearchConfigurationContext);
  console.log(useContext(SearchConfigurationContext));
  const multipleLayouts = layoutOptions.listView && layoutOptions.gridView;
  return (
    <React.Fragment>
      {(total || null) && (
        <>
          <Grid.Column textAlign="left" width={3}>
            <p>{i18next.t("Results: {{count}}", { count: total })}</p>
          </Grid.Column>
          <Grid.Column textAlign="right" width={13} floated="right">
            <div className="flex justify-end align-items-center">
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
            </div>
          </Grid.Column>
        </>
      )}
    </React.Fragment>
  );
};
