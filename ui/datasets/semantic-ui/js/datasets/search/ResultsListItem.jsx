import React, { useContext, useState } from "react";
import PropTypes from "prop-types";
import { Item, Label, Grid, Button } from "semantic-ui-react";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";
import sanitizeHtml from "sanitize-html";
import { i18next } from "@translations/i18next";
import { getValueFromMultilingualArray } from "@js/oarepo_ui/util";
import { IdentifierBadge } from "@js/oarepo_ui/components/IdentifierBadge";
import _truncate from "lodash/truncate";

const formatName = (person) => {
  const lastName = person.family_name || "";
  const givenNames = person.given_names || [];

  if (givenNames.length === 0) {
    return lastName;
  }

  const formattedGivenNames = givenNames.join(" ");

  return `${lastName}, ${formattedGivenNames}`;
};

const Creatibutor = ({ creatibutor }) => {
  const isPerson = !!creatibutor.person;
  const role = creatibutor?.role?.labels?.[0]?.value;
  const identifiers = isPerson
    ? creatibutor.person.external_identifiers
    : creatibutor.organization.external_identifiers;
  const selectedIdentifier =
    Array.isArray(identifiers) && identifiers.length > 0
      ? identifiers.find(
          (identifier) =>
            identifier?.scheme?.toLowerCase() === "orcid" ||
            identifier?.scheme?.toLowerCase() === "ror"
        ) || identifiers[0]
      : null;
  const name = isPerson
    ? formatName({
        given_names: creatibutor.person.given_names,
        family_name: creatibutor.person.family_name,
      })
    : creatibutor.organization?.name?.value;

  return (
    <React.Fragment>
      {`${name}`}
      <IdentifierBadge identifier={selectedIdentifier} creatibutorName={name} />
      {role && `( ${role} )`}
    </React.Fragment>
  );
};

Creatibutor.propTypes = {
  creatibutor: PropTypes.shape({
    person: PropTypes.shape({
      given_names: PropTypes.arrayOf(PropTypes.string),
      family_name: PropTypes.string,
      external_identifiers: PropTypes.arrayOf(
        PropTypes.shape({
          scheme: PropTypes.string,
          value: PropTypes.string,
        })
      ),
    }),
    organization: PropTypes.shape({
      name: PropTypes.shape({
        value: PropTypes.string,
      }),
      external_identifiers: PropTypes.arrayOf(
        PropTypes.shape({
          scheme: PropTypes.string,
          value: PropTypes.string,
        })
      ),
    }),
    role: PropTypes.shape({
      labels: PropTypes.arrayOf(
        PropTypes.shape({
          value: PropTypes.string,
        })
      ),
    }),
  }).isRequired,
};

const Creatibutors = ({ creatibutors }) => {
  return (
    <>
      {creatibutors.map((creatibutor, index) => (
        <React.Fragment key={index}>
          <Creatibutor creatibutor={creatibutor} />
          {index < creatibutors.length - 1 ? "; " : null}
        </React.Fragment>
      ))}
    </>
  );
};

Creatibutors.propTypes = { creatibutors: PropTypes.array.isRequired };

const ResultsListItemComponent = ({ result }) => {
  const [showEntireAbstract, setShowEntireAbstract] = useState(false);

  const searchAppConfig = useContext(SearchConfigurationContext);

  const { allowedHtmlTags } = searchAppConfig;

  const title = result.metadata?.title || i18next.t("Missing title");

  const abstract =
    result.metadata?.descriptions?.find((desc) => desc.lang === "en")?.value ||
    getValueFromMultilingualArray(result.metadata?.descriptions || []);
  const subjects = result.metadata?.subjects || [];
  const creatibutors = result.metadata?.qualified_relations;
  const publicationDate = result.metadata?.publication_year;
  const language = result.metadata?.primary_language;
  const originalRepositories =
    result?.metadata?.is_described_by?.original_repositories?.map(
      (originalRepository) =>
        originalRepository.labels.find((label) => label.lang === "en")?.value ||
        getValueFromMultilingualArray(originalRepository.labels || [])
    ) || [];

  const toggleAbstract = () => {
    setShowEntireAbstract(!showEntireAbstract);
  };

  const truncatedAbstract = abstract
    ? showEntireAbstract
      ? abstract
      : _truncate(abstract, { length: 500, separator: /,?\.* +/ })
    : "";

  return (
    <Item className="results-list-item-main">
      <Item.Content>
        <Grid className="m-0">
          <Grid.Row columns={2}>
            <Grid.Column width={13}>
              <Item.Header as="h2">
                <a href={result?.links?.self_html}>{title}</a>
              </Item.Header>
              <Item.Meta className="rel-mt-1">
                <Creatibutors creatibutors={creatibutors} />
                <Label.Group className="rel-mt-1">
                  {subjects.map((subject, index) => (
                    <Label
                      className="subjects"
                      key={`${index}.${subject.title.value}`}
                    >
                      {subject.title.value}
                    </Label>
                  ))}
                </Label.Group>
              </Item.Meta>
              {abstract && (
                <Item.Description className="rel-mt-1">
                  <div
                    dangerouslySetInnerHTML={{
                      __html: sanitizeHtml(truncatedAbstract, {
                        allowedTags: allowedHtmlTags,
                        allowedAttributes: {},
                      }),
                    }}
                    className="inline"
                  />
                  {abstract.length > 500 && (
                    <Button
                      compact
                      size="tiny"
                      onClick={toggleAbstract}
                      className="transparent ml-5"
                    >
                      {showEntireAbstract
                        ? i18next.t("(show less)")
                        : i18next.t("(show more)")}
                    </Button>
                  )}
                </Item.Description>
              )}
              <Item.Extra className="rel-mt-1">
                <p>
                  {publicationDate && <span>{publicationDate}</span>}
                  {originalRepositories?.map((originalRepository, index) => (
                    <p className="rel-ml-1" key={originalRepository.id}>
                      <span>{originalRepository}</span>
                      {index < originalRepositories.length - 1 ? ", " : null}
                    </p>
                  ))}
                  {language && (
                    <span className="rel-ml-1">{language.toUpperCase()}</span>
                  )}
                </p>
              </Item.Extra>
            </Grid.Column>
            <Grid.Column width={3}></Grid.Column>
          </Grid.Row>
        </Grid>
      </Item.Content>
    </Item>
  );
};

ResultsListItemComponent.propTypes = {
  result: PropTypes.object.isRequired,
};

export default ResultsListItemComponent;
