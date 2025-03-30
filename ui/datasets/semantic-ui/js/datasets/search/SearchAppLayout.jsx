import React, { useContext, useState, useEffect } from "react";
import PropTypes from "prop-types";
import _isEmpty from "lodash/isEmpty";
import Overridable from "react-overridable";
import { withState, ActiveFilters } from "react-searchkit";
import { GridResponsiveSidebarColumn } from "react-invenio-forms";
import {
  Container,
  Grid,
  Button,
  Label,
  Icon,
  TransitionablePortal,
} from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import {
  SearchAppFacets,
  SearchAppResultsPane,
  SearchBar,
  SearchConfigurationContext,
} from "@js/invenio_search_ui/components";
import { ResultOptions } from "./ResultOptions";
import {
  ShouldActiveFiltersRender,
  ClearFiltersButton,
} from "@js/oarepo_ui/search";
import { useActiveSearchFilters } from "@js/oarepo_ui/search/hooks";

const ResultOptionsWithState = withState(ResultOptions);

export const ActiveFiltersCountFloatingLabelComponent = ({
  currentQueryState: { filters },
  className,
}) => {
  const activeFiltersNumber = useActiveSearchFilters(filters)?.length;

  return (
    activeFiltersNumber > 0 && (
      <Label floating circular size="mini" className={className}>
        {activeFiltersNumber}
      </Label>
    )
  );
};

ActiveFiltersCountFloatingLabelComponent.propTypes = {
  className: PropTypes.string,
  currentQueryState: PropTypes.object.isRequired,
};

ActiveFiltersCountFloatingLabelComponent.defaultProps = {
  className: "active-filters-count-label",
};

export const ActiveFiltersCountFloatingLabel = withState(
  ActiveFiltersCountFloatingLabelComponent
);

export const SearchAppResultsGrid = ({
  columnsAmount,
  facetsAvailable,
  config,
  appName,
  buildUID,
  resultsPaneLayout,
  hasButtonSidebar,
  resultSortLayout,
}) => {
  const [sidebarVisible, setSidebarVisible] = useState(false);

  return (
    <Grid
      columns={columnsAmount}
      relaxed
      className="search-app rel-mt-2"
      padded
    >
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
          <ShouldActiveFiltersRender>
            <ClearFiltersButton
              className={"clear-filters-button mobile tablet only"}
              icon={null}
              labelPosition={null}
            />
          </ShouldActiveFiltersRender>
          <SearchAppFacets
            aggs={config.aggs}
            appName={appName}
            buildUID={buildUID}
          />
        </GridResponsiveSidebarColumn>
      )}
      <Grid.Column {...resultsPaneLayout}>
        <Grid className="subgrid">
          <Grid.Row width={16}>
            {facetsAvailable && (
              <Grid.Column
                floated="left"
                only="mobile tablet"
                mobile={2}
                tablet={2}
                textAlign="center"
              >
                <Button
                  basic
                  onClick={() => setSidebarVisible(true)}
                  title={i18next.t("Filter results")}
                  aria-label={i18next.t("Filter results")}
                  className="facets-sidebar-open-button"
                >
                  <Icon name="filter"></Icon>
                  <ShouldActiveFiltersRender>
                    <ActiveFiltersCountFloatingLabel />
                  </ShouldActiveFiltersRender>
                </Button>
              </Grid.Column>
            )}
            <Grid.Column width={14} floated="right" only="mobile tablet">
              <SearchBar buildUID={buildUID} appName={appName} />
              <p className="right-floated">
                {i18next.t(
                  "TIP: Most content is in English language. You will find more results by using English terminology."
                )}
              </p>
            </Grid.Column>
            <Grid.Column width={16} floated="right" only="computer">
              <SearchBar buildUID={buildUID} appName={appName} />
              <p className="right-floated">
                <em>
                  {i18next.t(
                    "TIP: Most content is in English language. You will find more results by using English terminology."
                  )}
                </em>
              </p>
            </Grid.Column>
          </Grid.Row>
          <ShouldActiveFiltersRender>
            <Grid.Row only="computer tablet">
              {facetsAvailable && <ActiveFilters />}
            </Grid.Row>
          </ShouldActiveFiltersRender>
          <Grid.Row verticalAlign="middle" className="result-options pb-0">
            <ResultOptionsWithState />
          </Grid.Row>
          <Grid.Row verticalAlign="middle">
            <SearchAppResultsPane
              layoutOptions={config.layoutOptions}
              appName={appName}
              buildUID={buildUID}
            />
          </Grid.Row>
        </Grid>
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
    </Grid>
  );
};

SearchAppResultsGrid.propTypes = {
  columnsAmount: PropTypes.number.isRequired,

  facetsAvailable: PropTypes.bool.isRequired,
  config: PropTypes.shape({
    aggs: PropTypes.array.isRequired,
    layoutOptions: PropTypes.object,
  }).isRequired,
  appName: PropTypes.string.isRequired,
  buildUID: PropTypes.func.isRequired,
  resultsPaneLayout: PropTypes.object.isRequired,
  hasButtonSidebar: PropTypes.bool,
  resultSortLayout: PropTypes.object.isRequired,
};
export const SearchAppLayout = ({ config, hasButtonSidebar }) => {
  const { appName, buildUID } = useContext(SearchConfigurationContext);
  const facetsAvailable = !_isEmpty(config.aggs);
  let columnsAmount;
  let resultsPaneLayoutFacets;

  const [scrollToTopVisible, setScrollToTopVisible] = React.useState(false);

  useEffect(() => {
    const handleScrollButtonVisibility = () => {
      window.scrollY > 300
        ? setScrollToTopVisible(true)
        : setScrollToTopVisible(false);
      window.scroll;
    };

    window.addEventListener("scroll", handleScrollButtonVisibility);

    return () => {
      window.removeEventListener("scroll", handleScrollButtonVisibility);
    };
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

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
    mobile: 14,
    tablet: 14,
    computer: 5,
    largeScreen: 5,
    widescreen: 5,
  };

  const resultsSortLayoutNoFacets = {
    mobile: 16,
    tablet: 16,
    computer: 16,
    largeScreen: 16,
    widescreen: 16,
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
      <SearchAppResultsGrid
        columnsAmount={columnsAmount}
        facetsAvailable={facetsAvailable}
        config={config}
        appName={appName}
        buildUID={buildUID}
        resultsPaneLayout={resultsPaneLayout}
        hasButtonSidebar={hasButtonSidebar}
        resultSortLayout={resultSortLayout}
      />
      <TransitionablePortal
        open={scrollToTopVisible}
        transition={{ animation: "fade up", duration: 300 }}
      >
        <Button
          onClick={scrollToTop}
          id="scroll-to-top-button"
          primary
          circular
          basic
        >
          <div>
            <Icon size="large" name="chevron up" />
          </div>
          <div className="scroll-to-top-text">
            {i18next.t("to top").toUpperCase()}
          </div>
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
    aggs: PropTypes.array,
  }),
  hasButtonSidebar: PropTypes.bool,
};
