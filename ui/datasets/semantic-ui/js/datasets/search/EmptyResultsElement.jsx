import React from "react";
import PropTypes from "prop-types";
import { i18next as OArepoUIi18next } from "@translations/oarepo_ui/i18next";
import { i18next } from "@translations/i18next";
import { Button, Icon, Segment, Grid, Divider } from "semantic-ui-react";

export const EmptyResultsElement = ({
  queryString = "",
  resetQuery,
  extraContent = null,
}) => {
  return (
    <Segment placeholder textAlign="center">
      <Grid columns={1} centered>
        <Grid.Row>
          <Icon name="search" size="huge" color="primary" />
        </Grid.Row>
        {queryString && (
          <Grid.Row as="em">
            {OArepoUIi18next.t("We couldn't find any matches for ")} "{queryString}"
          </Grid.Row>
        )}
        <Grid.Row>
          <Button primary onClick={() => resetQuery()}>
            {OArepoUIi18next.t("Start over")}
          </Button>
        </Grid.Row>
        <Divider horizontal>{OArepoUIi18next.t("or")}</Divider>
        <Grid.Row>
          <Button as="a" primary href="/datasets/uploads/new">
            {i18next.t("Register a Dataset")}
          </Button>
        </Grid.Row>
        {extraContent && (
          <Grid.Row>
            {extraContent}
          </Grid.Row>)
        }
      </Grid>
    </Segment>
  );
};

EmptyResultsElement.propTypes = {
  // eslint-disable-next-line react/require-default-props
  queryString: PropTypes.string,
  resetQuery: PropTypes.func.isRequired,
  // eslint-disable-next-line react/require-default-props
  extraContent: PropTypes.node,
};
