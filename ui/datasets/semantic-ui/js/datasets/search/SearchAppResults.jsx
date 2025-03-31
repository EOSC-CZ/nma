import React from "react";
import { Grid } from "semantic-ui-react";
import { ResultsList, Pagination } from "react-searchkit";

export const SearchAppResults = () => {
  return (
    <Grid relaxed>
      <Grid.Row>
        <Grid.Column>
          <ResultsList />
        </Grid.Column>
      </Grid.Row>
      <Grid.Row verticalAlign="middle" className="pt-0">
        <Grid.Column width={16} textAlign="right" floated="right">
          <Pagination />
        </Grid.Column>
      </Grid.Row>
    </Grid>
  );
};
