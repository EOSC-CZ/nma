import React, { useContext } from "react";
import PropTypes from "prop-types";
import { Item, Label, List, Grid } from "semantic-ui-react";
import { Image } from "react-invenio-forms";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";
import sanitizeHtml from "sanitize-html";

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
    ? creatibutor.person.identifiers
    : creatibutor.organization.identifiers;

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
      identifiers: PropTypes.arrayOf(
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
      identifiers: PropTypes.arrayOf(
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
  const searchAppConfig = useContext(SearchConfigurationContext);

  const { allowedHtmlTags } = searchAppConfig;
  const title = result.metadata?.title || "No title";
  const abstract =
    result.metadata?.descriptions?.find((desc) => desc.lang === "en")?.value ||
    result.metadata?.descriptions?.[0]?.value;
  const subjects = result.metadata?.subjects || [];
  const creatibutors = result.metadata?.qualified_relations;
  const publicationDate = result.metadata?.publication_year || "N/A";
  const language = result.metadata?.primary_language;
  const originalRepositories =
    result?.metadata?.is_described_by?.original_repositories?.map(
      (originalRepository) =>
        (
          originalRepository.labels.find((label) => label.lang === "en") ||
          originalRepository.labels[0]
        ).value
    ) || [];
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
                    <Label key={index}>{subject.title.value}</Label>
                  ))}
                </Label.Group>
              </Item.Meta>
              {abstract && (
                <Item.Description
                  className="rel-mt-1"
                  dangerouslySetInnerHTML={{
                    __html: sanitizeHtml(abstract, {
                      allowedTags: allowedHtmlTags,
                      allowedAttributes: {},
                    }),
                  }}
                />
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
            {/* this whole section needs discussion */}
            <Grid.Column width={3}>
              <List>
                <List.Item>
                  <Label>License</Label>
                </List.Item>
                <List.Item>
                  <Label>Počet souborů</Label>
                </List.Item>
                <List.Item>
                  <Label>Verze: {result.metadata?.version}</Label>
                </List.Item>
                <List.Item>
                  <Label>Typ souboru</Label>
                </List.Item>
                <List.Item>
                  <Label>Originál záznam</Label>
                </List.Item>
              </List>
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

export const IconIdentifier = ({ link, badgeTitle, icon, alt, className }) => {
  return link ? (
    <span className={`creatibutor-identifier ${className}`}>
      <a
        className="no-text-decoration mr-0"
        href={link}
        aria-label={badgeTitle}
        title={badgeTitle}
        key={link}
        target="_blank"
        rel="noopener noreferrer"
      >
        <Image
          className="inline-id-icon identifier-badge inline"
          src={icon}
          alt={alt}
        />
      </a>
    </span>
  ) : (
    <span className={`creatibutor-identifier ${className}`}>
      <Image
        title={badgeTitle}
        className="inline-id-icon identifier-badge inline"
        src={icon}
        alt={alt}
      />
    </span>
  );
};

IconIdentifier.propTypes = {
  link: PropTypes.string,
  badgeTitle: PropTypes.string,
  icon: PropTypes.string,
  alt: PropTypes.string,
  className: PropTypes.string,
};

export const IdentifierBadge = ({ identifier, creatibutorName, className }) => {
  if (!identifier) return null;

  const { scheme, identifier: identifierValue, url } = identifier;

  const badgeTitle = `${creatibutorName} ${scheme}: ${identifierValue}`;

  const lowerCaseScheme = scheme?.toLowerCase();

  return (
    <IconIdentifier
      link={url}
      badgeTitle={badgeTitle}
      icon={`/static/images/identifiers/${lowerCaseScheme}.svg`}
      alt={`${scheme.toUpperCase()} logo`}
      className={className}
    />
  );
};

IdentifierBadge.propTypes = {
  identifier: PropTypes.shape({
    scheme: PropTypes.string,
    identifier: PropTypes.string,
    url: PropTypes.string,
  }),
  className: PropTypes.string,
  creatibutorName: PropTypes.string,
};
