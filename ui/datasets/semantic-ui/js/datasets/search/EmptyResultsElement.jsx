import React from "react";
import PropTypes from "prop-types";
import { i18next as OArepoUIi18next } from "@translations/oarepo_ui/i18next";
import { i18next } from "@translations/i18next";
import {
  Button,
  Icon,
  Segment,
  Grid,
  Divider,
  Header,
} from "semantic-ui-react";

export const EmptyResultsElement = ({
  queryString,
  searchPath,
  resetQuery,
  extraContent = null,
}) => {
  return (
    <Grid centered>
      <Grid.Row>
        <Grid.Column width={12} textAlign="center">
          <Header as="h2">
            {i18next.t("We couldn't find any matches for {{- search}}", {
              search:
                (queryString && `'${queryString}'`) || i18next.t("your search"),
            })}
          </Header>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row>
        <Button primary onClick={resetQuery}>
          <Icon name="search" />
          {i18next.t("Start over")}
        </Button>
      </Grid.Row>
      <Grid.Row>
        <Grid.Column width={8}>
          <Divider horizontal fitted>
            {OArepoUIi18next.t("or")}
          </Divider>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row>
        <Button as="a" primary href="/datasets/uploads/new">
          <Icon name="add" />
          {i18next.t("Register a Dataset")}
        </Button>
      </Grid.Row>
      {extraContent && <Grid.Row>{extraContent}</Grid.Row>}
      <Grid.Row>
        <Grid.Column width={12}>
          <Segment secondary padded size="large">
            <Header as="h3" size="small">
              {i18next.t("ProTip")}!
            </Header>
            <p>
              <a
                href={`${searchPath}?q=metadata.publication_date:[2025-01-01 TO *]`}
              >
                metadata.publication_date:[2025-01-01 TO *]
              </a>{" "}
              {i18next.t(
                "will give you all the publications from 2025 until today."
              )}
            </p>
            <p>
              {i18next.t("For more tips, check out our ")}{" "}
              <a href="/help/search" title={i18next.t("Search guide")}>
                {i18next.t("search guide")}
              </a>{" "}
              {i18next.t("for defining advanced search queries.")}
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
  searchPath: "/datasets",
};
