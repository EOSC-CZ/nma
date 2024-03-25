import React from "react";
import PropTypes from "prop-types";

import { Grid, Header, Button, Icon, Segment } from "semantic-ui-react";
import { i18next } from "@translations/i18next";

export const EmptyResultsElement = ({
  queryString,
  searchPath,
  resetQuery,
}) => {
  return (
    <Grid>
      <Grid.Row centered>
        <Grid.Column width={12} textAlign="center">
          <Header as="h2">
            {i18next.t("We couldn't find any matches for ")}
            {(queryString && `'${queryString}'`) || i18next.t("your search")}
          </Header>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row centered>
        <Grid.Column width={8} textAlign="center">
          <Button primary onClick={resetQuery}>
            <Icon name="search" />
            {i18next.t("Start over")}
          </Button>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row centered>
        <Grid.Column width={12}>
          <Segment secondary padded size="large">
            <Header as="h3" size="small">
              {i18next.t("ProTip")}!
            </Header>
            <p>
              <a
                href={`${searchPath}?q=metadata.publication_date:[2017-01-01 TO *]`}
              >
                metadata.publication_date:[2017-01-01 TO *]
              </a>{" "}
              {i18next.t(
                "will give you all the publications from 2017 until today."
              )}
            </p>
            <p>
              {i18next.t("For more tips, check out our ")}
              <a href="/help/search" title={i18next.t("Search guide")}>
                {i18next.t("search guide")}
              </a>
              {i18next.t(" for defining advanced search queries.")}
            </p>
          </Segment>
        </Grid.Column>
      </Grid.Row>
    </Grid>
  );
};

EmptyResultsElement.propTypes = {
  queryString: PropTypes.string.isRequired,
  resetQuery: PropTypes.func.isRequired,
  searchPath: PropTypes.string,
};

EmptyResultsElement.defaultProps = {
  searchPath: "",
};
