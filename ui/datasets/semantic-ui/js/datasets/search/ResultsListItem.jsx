import React, { useContext, useState } from "react";
import PropTypes from "prop-types";
import { Item, Label, Grid, Button, Icon } from "semantic-ui-react";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";
import sanitizeHtml from "sanitize-html";
import { i18next } from "@translations/i18next";
import { getValueFromMultilingualArray } from "@js/oarepo_ui/util";
import _truncate from "lodash/truncate";
import { Creatibutors } from "./Creatibutors";
import { ResultsItemAccessStatus } from "./ResultsItemAccessStatus";

const getDescription = (metadata) => {
  if (metadata?.description) {
    return metadata.description;
  }

  const descriptions = metadata?.additional_descriptions || metadata?.descriptions;
  if (Array.isArray(descriptions)) {
    const byDescription = descriptions.find((desc) => desc?.description);
    if (byDescription?.description) {
      return byDescription.description;
    }

    const byValue = descriptions.find((desc) => desc?.value);
    if (byValue?.value) {
      return byValue.value;
    }
  }

  return "";
};

const resolveSubjectLabel = (subject) => {
  if (!subject) {
    return "";
  }

  if (typeof subject === "string") {
    return subject;
  }

  const titleObj = subject.title;
  if (titleObj && typeof titleObj === "object" && !Array.isArray(titleObj)) {
    return (
      titleObj[i18next.language] ||
      titleObj.en ||
      titleObj.cs ||
      Object.values(titleObj)[0]
    );
  }

  if (Array.isArray(titleObj)) {
    return titleObj[0] || subject.subject || subject.id;
  }

  return subject.subject || subject.id || "";
};

const resolveLanguageLabel = (language) => {
  if (!language) {
    return "";
  }

  if (typeof language === "string") {
    return language;
  }

  if (language.title && typeof language.title === "object") {
    return (
      language.title[i18next.language] ||
      language.title.en ||
      language.title.cs ||
      Object.values(language.title)[0]
    );
  }

  return language.title || language.id || "";
};

const resolvePublicationDate = (metadata, fallbackDate) => {
  if (metadata?.publication_date) {
    return metadata.publication_date;
  }

  if (Array.isArray(metadata?.dates)) {
    const issued = metadata.dates.find(({ type }) =>
      type?.id?.toLowerCase() === "issued" || type?.id?.toLowerCase() === "publication"
    );
    if (issued?.date) {
      return issued.date;
    }
  }

  return fallbackDate;
};

export const ResultsListItem = ({ result }) => {
  const [showEntireAbstract, setShowEntireAbstract] = useState(false);
  const searchAppConfig = useContext(SearchConfigurationContext);
  const { allowedHtmlTags } = searchAppConfig;

  const metadata = result.metadata || {};
  const title = metadata.title || i18next.t("Missing title");
  const description = getDescription(metadata);

  const abstract = sanitizeHtml(description, {
    allowedTags: allowedHtmlTags,
    allowedAttributes: {},
    disallowedTagsMode: "discard",
  });

  const subjects = metadata.subjects || [];
  const creators = metadata.creators || [];
  const contributors = metadata.contributors || [];
  const creatibutors = [...creators, ...contributors];
  const publicationDate = resolvePublicationDate(metadata, result.created);

  const languages = metadata.languages || (metadata.language ? [metadata.language] : []);
  const language = languages[0];
  // const accessStatus =
  //   result.ui?.access_status ||
  //   result.access?.status ||
  //   result.access?.record ||
  //   result.access?.files;

  const toggleAbstract = () => {
    setShowEntireAbstract(!showEntireAbstract);
  };

  const truncatedAbstract = abstract
    ? showEntireAbstract
      ? abstract
      : _truncate(abstract, { length: 500 })
    : "";

  return (
    <Item className="results-list-item-main">
      <Item.Content>
        <Grid className="m-0">
          <Grid.Row columns={2}>
            <Grid.Column width={16}>
              <Item.Header as="h2">
                <a href={result?.links?.self_html}>{title}</a>
              </Item.Header>
              <Item.Meta>
                <Creatibutors creatibutors={creatibutors} />
                <Label.Group className="rel-mt-1">
                  {subjects.map((subject, index) => (
                    <Label className="subjects" key={`${index}.${subject?.id || resolveSubjectLabel(subject)}`}>
                      {resolveSubjectLabel(subject)}
                    </Label>
                  ))}
                </Label.Group>
              </Item.Meta>
              {abstract && (
                <Item.Description className="rel-mt-1">
                  <div
                    dangerouslySetInnerHTML={{
                      __html: truncatedAbstract,
                    }}
                    className="inline"
                  />
                  {abstract.length > 500 && (
                    <Button
                      compact
                      size="tiny"
                      onClick={toggleAbstract}
                      className="transparent mr-3"
                    >
                      {showEntireAbstract ? (
                        <Icon name="left chevron" color="green" />
                      ) : (
                        <Icon name="right chevron" color="green" />
                      )}
                    </Button>
                  )}
                </Item.Description>
              )}
              <Item.Extra className="rel-mt-1">
                <p>
                  {publicationDate && (
                    <span className="rel-mr-1">
                      {i18next.t("Published")}: {publicationDate}
                    </span>
                  )}

                  {language && language?.id !== "UND" && (
                    <span className="rel-mr-1">
                      {i18next.t("Language")}: {resolveLanguageLabel(language)}
                    </span>
                  )}
                </p>
              </Item.Extra>
            </Grid.Column>
          </Grid.Row>
        </Grid>
      </Item.Content>
    </Item>
  );
};

ResultsListItem.propTypes = {
  result: PropTypes.object.isRequired,
};

export default ResultsListItem;
