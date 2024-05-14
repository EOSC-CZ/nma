import React, { useContext, useEffect } from "react";
import PropTypes from "prop-types";
import _isEmpty from "lodash/isEmpty";
import Overridable from "react-overridable";
import { withState, ActiveFilters, ResultsPerPage } from "react-searchkit";
import { GridResponsiveSidebarColumn } from "react-invenio-forms";
import { Container, Grid, Button, Header, TransitionablePortal, Icon } from "semantic-ui-react";
import { i18next as i18nOARepo } from "@translations/oarepo_ui/i18next";
import { i18next } from "@translations/i18next";
import {
  SearchAppFacets,
  SearchAppResultsPane,
  SearchBar,
  SearchConfigurationContext,
} from "@js/invenio_search_ui/components";
import { ResultOptions } from "@js/invenio_search_ui/components/Results";
import { ClearFiltersButton, ResultCountWithState, ResultsPerPageLabel } from "@datasets_search";

const ResultOptionsWithState = withState(ResultOptions);

export const SearchAppLayout = ({ config, hasButtonSidebar }) => {
  const [sidebarVisible, setSidebarVisible] = React.useState(false);
  const [scrollToTopVisible, setScrollToTopVisible] = React.useState(false);
  // console.log(useContext(SearchConfigurationContext));
  const { appName, buildUID, paginationOptions: { resultsPerPage } } = useContext(SearchConfigurationContext);

  useEffect(() => {
    const handleScrollButtonVisibility = () => {
      window.scrollY > 300 ? setScrollToTopVisible(true) : setScrollToTopVisible(false);
      window.scroll
    };

    window.addEventListener("scroll", handleScrollButtonVisibility);

    return () => {
      window.removeEventListener("scroll", handleScrollButtonVisibility);
    };
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

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
        mobile: 14,
        tablet: 14,
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
    computer: 11,
    largeScreen: 11,
    widescreen: 11,
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
              <ClearFiltersButton />
            )}
          </Grid.Column>
          <Grid.Column {...resultsPaneLayout}>
            <SearchBar buildUID={buildUID} appName={appName} />
            {facetsAvailable && (
              <ActiveFilters />
            )}
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
                title={i18nOARepo.t("Filter results")}
                aria-label={i18nOARepo.t("Filter results")}
              />
            </Grid.Column>
          )}
          <Grid.Column only="computer" width={4}>
            {facetsAvailable && (
              <Grid.Row>
                <Header size="medium" id="search-filters-header-title">{i18nOARepo.t("Filters")}</Header>
              </Grid.Row>
            )}
          </Grid.Column>
          <Grid.Column {...resultsPaneLayout}>
            <Grid as={Grid.Row} verticalAlign="middle" stackable>
              <Grid.Column floated="left" textAlign="left" verticalAlign="middle" width={2}>
                <ResultCountWithState />
              </Grid.Column>
              <Grid.Column  floated="right" textAlign="right" width={14}>
                <ResultsPerPage
                  values={resultsPerPage}
                  label={ResultsPerPageLabel}
                />
                <ResultOptionsWithState />
              </Grid.Column>
            </Grid>
          </Grid.Column>
        </Grid.Row>
        <Grid.Row columns={columnsAmount} className="facets-and-search-listing">
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
      <TransitionablePortal
        open={scrollToTopVisible}
        transition={{ animation: "fade up", duration: 300 }}
      >
        <Button
          onClick={scrollToTop}
          id="scroll-to-top-button"
          color="teal"
          circular
          basic
        >
          <div><Icon size="large" name="chevron up" /></div>
          <div className="scroll-to-top-text">{i18next.t("to top").toUpperCase()}</div>
        </Button>
      </TransitionablePortal>
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
