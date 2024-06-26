import React from "react";
import { Grid } from "semantic-ui-react";
import {
  ResultsList,
  Pagination,
  ResultsMultiLayout,
  ResultsGrid,
  withState,
} from "react-searchkit";
import PropTypes from "prop-types";

const SearchAppResultsComponent = ({
  layoutOptions,
}) => {
  const multipleLayouts = layoutOptions.listView && layoutOptions.gridView;
  const listOrGridView = layoutOptions.listView ? (
    <ResultsList />
  ) : (
    <ResultsGrid />
  );

  return (
    <Grid relaxed>
      <Grid.Row>
        <Grid.Column>
          {multipleLayouts ? <ResultsMultiLayout /> : listOrGridView}
        </Grid.Column>
      </Grid.Row>
      <Grid.Row verticalAlign="middle" textAlign="right">
        <Grid.Column
          className="computer tablet only"
          width={16}
          textAlign="right"
        >
          <Pagination
            options={{
              size: "tiny",
              showFirst: false,
              showLast: false,
            }}
          />
        </Grid.Column>
        <Grid.Column className="mobile only" width={16} textAlign="center">
          <Pagination
            options={{
              size: "tiny",
              boundaryRangeCount: 0,
              showFirst: false,
              showLast: false,
            }}
          />
        </Grid.Column>
      </Grid.Row>
    </Grid>
  );
};

SearchAppResultsComponent.propTypes = {
  paginationOptions: PropTypes.object.isRequired,
  layoutOptions: PropTypes.object.isRequired,
  currentResultsState: PropTypes.shape({
    data: PropTypes.shape({
      total: PropTypes.number.isRequired,
    }).isRequired,
  }).isRequired,
};

const SearchAppResults = withState(SearchAppResultsComponent);

export default SearchAppResults;
