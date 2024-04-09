import React, { useContext } from "react";
import PropTypes from "prop-types";
import _isEmpty from "lodash/isEmpty";
import Overridable from "react-overridable";
import { withState, ActiveFilters, ResultsPerPage } from "react-searchkit";
import { GridResponsiveSidebarColumn } from "react-invenio-forms";
import { Container, Grid, Button } from "semantic-ui-react";
import { i18next } from "@translations/oarepo_ui/i18next";
import {
  SearchAppFacets,
  SearchAppResultsPane,
  SearchBar,
  SearchConfigurationContext,
} from "@js/invenio_search_ui/components";
import { ResultOptions } from "@js/invenio_search_ui/components/Results";
import { ResultsPerPageLabel } from '@js/oarepo_ui/search';
import { ClearFiltersButton } from "@datasets_search";

const ResultOptionsWithState = withState(ResultOptions);

export const SearchAppLayout = ({ config, hasButtonSidebar }) => {
  const [sidebarVisible, setSidebarVisible] = React.useState(false);
  // console.log(useContext(SearchConfigurationContext));
  const { appName, buildUID, paginationOptions: { resultsPerPage } } = useContext(SearchConfigurationContext);
  const facetsAvailable = !_isEmpty(config.aggs);

  let columnsAmount;
  let resultsPaneLayoutFacets;

  if (facetsAvailable) {
    if (hasButtonSidebar) {
      columnsAmount = 3;
      resultsPaneLayoutFacets = {
        mobile: 16,
        tablet: 16,
        computer: 10,
        largeScreen: 10,
        widescreen: 10,
        width: undefined,
      };
    } else {
      columnsAmount = 2;
      resultsPaneLayoutFacets = {
        mobile: 16,
        tablet: 16,
        computer: 12,
        largeScreen: 12,
        widescreen: 12,
        width: undefined,
      };
    }
  } else {
    if (hasButtonSidebar) {
      columnsAmount = 2;
      resultsPaneLayoutFacets = {
        mobile: 16,
        tablet: 16,
        computer: 12,
        largeScreen: 12,
        widescreen: 12,
        width: undefined,
      };
    } else {
      columnsAmount = 1;
      resultsPaneLayoutFacets = {
        mobile: 16,
        tablet: 16,
        computer: 16,
        largeScreen: 16,
        widescreen: 16,
        width: undefined,
      };
    }
  }

  const resultsSortLayoutFacets = {
    mobile: 11,
    tablet: 11,
    computer: 12,
    largeScreen: 12,
    widescreen: 12,
  };

  const resultsSortLayoutNoFacets = {
    mobile: 12,
    tablet: 12,
    computer: 12,
    largeScreen: 12,
    widescreen: 12,
  };

  const resultsPaneLayoutNoFacets = resultsPaneLayoutFacets;

  // make list full width if no facets available
  const resultsPaneLayout = facetsAvailable
    ? resultsPaneLayoutFacets
    : resultsPaneLayoutNoFacets;

  const resultSortLayout = facetsAvailable
    ? resultsSortLayoutFacets
    : resultsSortLayoutNoFacets;

  return (
    <Container fluid>
      <Grid
        columns={columnsAmount}
        relaxed
        className="search-app"
      >
        <Grid.Row>
          <Grid.Column only="computer" width={4}>
            {facetsAvailable && (
              <ActiveFilters />
            )}
          </Grid.Column>
          <Grid.Column {...resultsPaneLayout}>
            <SearchBar buildUID={buildUID} appName={appName} />
          </Grid.Column>
        </Grid.Row>
        <Grid.Row verticalAlign="middle" className="result-options">
          {facetsAvailable && (
            <Grid.Column
              floated="left"
              only="mobile tablet"
              mobile={1}
              tablet={1}
              textAlign="center"
              className="rel-mr-1"
            >
              <Button
                basic
                icon="sliders"
                onClick={() => setSidebarVisible(true)}
                title={i18next.t("Filter results")}
                aria-label={i18next.t("Filter results")}
              />
            </Grid.Column>
          )}
          <Grid.Column mobile={4} tablet={4} stretched>
            <ClearFiltersButton />
          </Grid.Column>
          <Grid.Column textAlign="right" floated="right" {...resultSortLayout}>
            <Grid.Row >
              <ResultsPerPage 
                values={resultsPerPage} 
                label={ResultsPerPageLabel} 
              />
              <ResultOptionsWithState />
            </Grid.Row>
          </Grid.Column>
        </Grid.Row>
        <Grid.Row columns={columnsAmount}>
          {facetsAvailable && (
            <GridResponsiveSidebarColumn
              mobile={4}
              tablet={4}
              computer={4}
              largeScreen={4}
              widescreen={4}
              open={sidebarVisible}
              onHideClick={() => setSidebarVisible(false)}
            >
              <SearchAppFacets
                aggs={config.aggs}
                appName={appName}
                buildUID={buildUID}
              />
            </GridResponsiveSidebarColumn>
          )}
          <Grid.Column {...resultsPaneLayout}>
            <SearchAppResultsPane
              layoutOptions={config.layoutOptions}
              appName={appName}
              buildUID={buildUID}
            />
          </Grid.Column>
          {hasButtonSidebar && (
            <Grid.Column
              mobile={16}
              tablet={16}
              computer={4}
              largeScreen={4}
              widescreen={4}
            >
              <Overridable
                id={buildUID("SearchApp.buttonSidebarContainer", "", appName)}
              ></Overridable>
            </Grid.Column>
          )}
        </Grid.Row>
      </Grid>
    </Container>
  );
};

SearchAppLayout.propTypes = {
  config: PropTypes.shape({
    searchApi: PropTypes.object.isRequired, // same as ReactSearchKit.searchApi
    initialQueryState: PropTypes.shape({
      queryString: PropTypes.string,
      sortBy: PropTypes.string,
      sortOrder: PropTypes.string,
      page: PropTypes.number,
      size: PropTypes.number,
      hiddenParams: PropTypes.array,
      layout: PropTypes.oneOf(["list", "grid"]),
    }),
  }),
};

export default SearchAppLayout;
