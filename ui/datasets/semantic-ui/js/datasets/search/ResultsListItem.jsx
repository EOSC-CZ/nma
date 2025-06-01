import React, { useContext, useState } from "react";
import PropTypes from "prop-types";
import { Item, Label, Grid, Button, Icon } from "semantic-ui-react";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";
import sanitizeHtml from "sanitize-html";
import { i18next } from "@translations/i18next";
import { getValueFromMultilingualArray } from "@js/oarepo_ui/util";
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
  const publicationDate = result.metadata?.time_references?.find(
    ({ date_type }) => date_type?.id === "issued"
  )?.date;
  const language = result.metadata?.primary_language;
  const originalRepositories = [];
  result?.metadata?.is_described_by?.forEach((describedBy) => {
    if (describedBy?.original_repositories?.length) {
      describedBy.original_repositories.forEach((repo) => {
        const repoName =
          repo.labels?.find((label) => label.lang === "en")?.value ||
          getValueFromMultilingualArray(repo.labels || []);

        if (repoName) {
          originalRepositories.push(repoName);
        }
      });
    }
  });

  const toggleAbstract = () => {
    setShowEntireAbstract(!showEntireAbstract);
  };

  const truncatedAbstract = abstract
    ? showEntireAbstract
      ? abstract
      : _truncate(abstract, { length: 500 })
    : "";

  // Find the first access_right in the terms_of_use array
  const accessStatus = result?.metadata?.terms_of_use?.find(
    (term) => term.access_rights
  )?.access_rights?.[0];

  return (
    <Item className="results-list-item-main">
      <Item.Content>
        <Grid className="m-0">
          <Grid.Row columns={2}>
            <Grid.Column width={16}>
              <Item.Header as="h2">
                <a href={result?.links?.self_html}>{title}</a>
              </Item.Header>
              {accessStatus && (
                <ResultsItemAccessStatus status={accessStatus} />
              )}
              <Item.Meta className="rel-mt-1">
                <Creatibutors creatibutors={creatibutors} />
                <Label.Group className="rel-mt-1">
                  {
                    // TODO: subject is multilingual, need to change model to reflect this
                    subjects.map((subject, index) => (
                      <Label
                        className="subjects"
                        key={`${index}.${subject.title[0]?.value}`}
                      >
                        {subject.title[0]?.value}
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
                  {originalRepositories?.length > 0 && (
                    <span className="rel-mr-1">
                      {i18next.t("Published in")}:{" "}
                      {originalRepositories?.map(
                        (originalRepository, index) => (
                          <span key={originalRepository.id}>
                            {originalRepository}
                            {index < originalRepositories.length - 1
                              ? ", "
                              : null}
                          </span>
                        )
                      )}
                    </span>
                  )}

                  {language && language?.id !== "UND" && (
                    <span>
                      {i18next.t("Language")}: {language?.title}
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

ResultsListItemComponent.propTypes = {
  result: PropTypes.object.isRequired,
};

export default ResultsListItemComponent;
