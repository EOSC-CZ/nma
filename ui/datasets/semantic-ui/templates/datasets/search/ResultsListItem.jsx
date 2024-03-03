import React, { useContext } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";

import _get from "lodash/get";

import { Grid, Item } from "semantic-ui-react";
import { withState, buildUID } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";

import { i18next } from "@translations/i18next";

const ItemHeader = ({ title, searchUrl, selfLink }) => {
  const viewLink = new URL(
    selfLink,
    new URL(searchUrl, window.location.origin)
  );
  return (
    <Item.Header as="h2">
      <a href={viewLink}>{title}</a>
    </Item.Header>
  );
};

const ItemSubheader = ({}) => {
  // just an example
  return (
    <>
      <Item.Meta>
        <Grid columns={1}>
          <Grid.Column>
            <Grid.Row className="ui double separated creatibutors"></Grid.Row>
          </Grid.Column>
        </Grid>
      </Item.Meta>
    </>
  );
};

export const ResultsListItemComponent = ({
  currentQueryState,
  result,
  appName,
  ...rest
}) => {
  const searchAppConfig = useContext(SearchConfigurationContext);

  const title = _get(result, "metadata.title", "<no title>");

  return (
    <Overridable
      id={buildUID("RecordsResultsListItem.layout", "", appName)}
      result={result}
      title={title}
      {...rest}
    >
      <Item key={result.id}>
        <Item.Content>
          <Grid>
            <Grid.Row columns={1}>
              <Grid.Column className="results-list item-main">
                <ItemHeader
                  title={title}
                  searchUrl={searchAppConfig.ui_endpoint}
                  selfLink={result.links.self}
                />
                <ItemSubheader />
                <Item.Description />
              </Grid.Column>
            </Grid.Row>
          </Grid>
        </Item.Content>
      </Item>
    </Overridable>
  );
};

ResultsListItemComponent.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

ResultsListItemComponent.defaultProps = {
  currentQueryState: null,
  appName: "",
};

export const ResultsListItem = (props) => {
  return (
    <Overridable id={buildUID("ResultsListItem", "", props.appName)} {...props}>
      <ResultsListItemComponent {...props} />
    </Overridable>
  );
};

ResultsListItem.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
  appName: PropTypes.string,
};

ResultsListItem.defaultProps = {
  currentQueryState: null,
  appName: "",
};

export const ResultsListItemWithState = withState(
  ({ currentQueryState, updateQueryState, result, appName }) => (
    <ResultsListItem
      currentQueryState={currentQueryState}
      updateQueryState={updateQueryState}
      result={result}
      appName={appName}
    />
  )
);

ResultsListItemWithState.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
};

ResultsListItemWithState.defaultProps = {
  currentQueryState: null,
};
