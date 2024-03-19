import React, { useContext } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import _get from "lodash/get";
import _join from "lodash/join";
import _truncate from "lodash/truncate";
import _find from "lodash/find";
import { Grid, Item, Label, List, Icon } from "semantic-ui-react";
import { withState, buildUID } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";
import { i18next } from "@translations/i18next";
import {
  ResultsItemRights,
  ResultsItemSubjects,
  ResultsItemCreatibutors,
  DoubleSeparator,
  ResultsItemResourceType,
} from "@datasets_search";

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

ItemHeader.propTypes = {
  title: PropTypes.string.isRequired,
  searchUrl: PropTypes.string.isRequired,
  selfLink: PropTypes.string.isRequired,
};

const ItemSubheader = ({
  creators,
  contributors,
  publicationDate,
  language,
  version,
  resourceType,
  thesis,
  searchUrl,
}) => {
  const isThesisDefended = thesis?.dateDefended;

  return (
    <Item.Meta>
      <Grid columns={1}>
        <Grid.Column>
          <Grid.Row className="ui double separated creatibutors">
            <ResultsItemCreatibutors
              creators={creators}
              contributors={contributors}
              searchUrl={searchUrl}
            />
          </Grid.Row>
          <Grid.Row className="ui separated">
            <span
              aria-label={i18next.t("Publication date")}
              title={i18next.t("Publication date")}
            >
              {publicationDate} (v{version})
            </span>
            {/* {language && 
            <>
              <DoubleSeparator />
              <span
                aria-label={i18next.t("Language")}
                title={i18next.t("Language")}
              >
                {language}
              </span>
            </>} */}
          </Grid.Row>
          <Grid.Row>
            <ResultsItemResourceType
              searchUrl={searchUrl}
              resourceType={resourceType}
            />
            {thesis && (
              <Label pointing="left" size="mini" basic>
                <Icon
                  name={isThesisDefended ? "check circle" : "remove circle"}
                  color={isThesisDefended ? "green" : "red"}
                />{" "}
                {isThesisDefended
                  ? i18next.t("defended")
                  : i18next.t("not defended")}
              </Label>
            )}
          </Grid.Row>
        </Grid.Column>
      </Grid>
    </Item.Meta>
  );
};

ItemSubheader.propTypes = {
  creators: PropTypes.array,
  contributors: PropTypes.array,
  publicationDate: PropTypes.string,
  language: PropTypes.string,
  version: PropTypes.number,
  resourceType: PropTypes.object,
  thesis: PropTypes.object,
  searchUrl: PropTypes.string,
};

const ItemExtraInfo = ({ createdDate, language, publisher }) => {
  return (
    <Item.Extra>
      <div>
        <small>
          <p>
            {createdDate && <span>{createdDate}</span>}
            {language && <span className="left-tab">{language.toUpperCase()}</span>}
            {publisher && <span className="left-tab">{publisher.name}</span>}
            <span className="left-tab">{i18next.t("National Metadata Repository")}</span>
          </p>
        </small>
      </div>
    </Item.Extra>
  );
};

ItemExtraInfo.propTypes = {
  createdDate: PropTypes.string,
  language: PropTypes.string,
  publisher: PropTypes.object,
};

const ItemSidebarIcons = ({ rights }) => {
  return (
    <Item.Extra className="labels-actions">
      <List horizontal>
        {rights.map(right => (
          <List.Item key={right.rights}>
            <ResultsItemRights right={right} />
          </List.Item>
        ))}
      </List>
    </Item.Extra>
  );
};

ItemSidebarIcons.propTypes = {
  rights: PropTypes.array,
};

export const ResultsListItemComponent = ({
  currentQueryState,
  result,
  appName,
  ...rest
}) => {
  const searchAppConfig = useContext(SearchConfigurationContext);

  console.log("SearchResult", result);
  console.log("SearchAppConfig", searchAppConfig);

  const accessRights = _get(result, "metadata.rightsList"); // fix
  const createdDate = _get(result, "created", "No creation date found.");
  const creators = result.metadata?.creators;
  const contributors = _get(result, "metadata.contributors", []);

  const descriptionStripped = _get(
    result,
    "metadata.descriptions[0].description",
    i18next.t("No description")
  );

  const language = _get(result, "metadata.language");
  console.log("Language", language);

  const publicationDate = _find(_get(
    result,
    "metadata.dates",
    []
  ), (date) => date.dateType.toLowerCase() === "issued").date ?? i18next.t("No publication date found.");
  const resourceTypeGeneral = _get(result, "metadata.types[0]"); // TODO: can there be more than one?
  const subjects = _get(result, "metadata.subjects", []);
  const title = _get(result, "metadata.titles[0].title", "No title");
  const version = _get(result, "revision_id", null); // TODO: revision_id or metadata.version?
  const versions = _get(result, "versions"); // TODO: What is this??

  const thesis = _get(result, "metadata.thesis"); // TODO: Remove??
  const publisher = _get(result, "metadata.publisher"); // TODO: only one

  const filters =
    currentQueryState && Object.fromEntries(currentQueryState.filters);
  const allVersionsVisible = filters?.allversions;
  const numOtherVersions = version - 1;

  return (
    <Overridable
      id={buildUID("RecordsResultsListItem.layout", "", appName)}
      result={result}
      accessStatus={accessRights}
      createdDate={createdDate}
      creators={creators}
      descriptionStripped={descriptionStripped}
      publicationDate={publicationDate}
      publisher={publisher}
      resourceType={resourceTypeGeneral}
      subjects={subjects}
      language={language}
      title={title}
      version={version}
      versions={versions}
      thesis={thesis}
      allVersionsVisible={allVersionsVisible}
      numOtherVersions={numOtherVersions}
    >
      <Item key={result.id}>
        <Item.Content>
          <Grid>
            <Grid.Row >
              <Grid.Row className="results-list item-main">
                {accessRights && <ItemSidebarIcons rights={accessRights} />}
                <ItemHeader
                  title={title}
                  searchUrl={searchAppConfig.ui_endpoint}
                  selfLink={result.links.self_html}
                />
                <ItemSubheader
                  creators={creators}
                  contributors={contributors}
                  publicationDate={publicationDate}
                  language={language}
                  version={version}
                  resourceType={resourceTypeGeneral}
                  thesis={thesis}
                  searchUrl={searchAppConfig.ui_endpoint}
                />
                <Item.Description>
                  {_truncate(descriptionStripped, { length: 350 })} 
                </Item.Description>
                <ResultsItemSubjects searchUrl={searchAppConfig.ui_endpoint} subjects={subjects} />
                <ItemExtraInfo
                  createdDate={createdDate}
                  language={language}
                  publishers={publisher}
                />
              </Grid.Row>
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

const ResultsListItemWithState = withState(
  ({ currentQueryState, updateQueryState, result, appName }) => (
    <ResultsListItem
      currentQueryState={currentQueryState}
      updateQueryState={updateQueryState}
      result={result}
      appName={appName}
    />
  )
);

export default ResultsListItemWithState;

ResultsListItemWithState.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
};

ResultsListItemWithState.defaultProps = {
  currentQueryState: null,
};
