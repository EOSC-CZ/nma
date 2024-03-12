import React from "react";
import { List } from "semantic-ui-react";
import { DoubleSeparator } from "./DoubleSeparator";
import { IconPersonIdentifier } from "./IconPersonIdentifier";
import { SearchFacetLink } from "./SearchFacetLink";
import _groupBy from "lodash/groupBy";
import _toPairs from "lodash/toPairs";
import _join from "lodash/join";
import { i18next } from "@translations/i18next";
import PropTypes from "prop-types";

const CreatibutorSearchLink = ({
  personName = "No name",
  searchField = "creators",
  searchUrl = "/",
}) => (
  <SearchFacetLink
    searchUrl={searchUrl}
    searchFacet={`metadata_${searchField}_fullName`}
    value={personName}
    className={`${searchField}-link`}
    title={`${personName}: ${i18next.t("Find more records by this person")}`}
    label={personName}
  />
);

CreatibutorSearchLink.propTypes = {
  personName: PropTypes.string,
  searchField: PropTypes.string,
  searchUrl: PropTypes.string,
};

const CreatibutorIcons = ({ personName = "No name", identifiers = [] }) =>
  identifiers.map((i) => (
    <IconPersonIdentifier
      key={`${i.scheme}:${i.identifier}`}
      identifier={i}
      personName={personName}
    />
  ));

CreatibutorIcons.propTypes = {
  personName: PropTypes.string,
  identifiers: PropTypes.array,
};

export function ResultsItemCreatibutors({
  creators = [],
  contributors = [],
  maxCreators = 3,
  maxContributors = 3,
  searchUrl,
  className,
}) {
  const uniqueContributors = _toPairs(
    _groupBy(
      contributors.slice(0, maxContributors),
      ({ fullName, authorityIdentifiers = [] }) => {
        const idKeys = _join(
          authorityIdentifiers.map((i) => `${i.scheme}:${i.identifier}`),
          ";"
        );
        return `${fullName}-${idKeys}`;
      }
    )
  ).map(([groupKey, entries]) => ({
    id: groupKey,
    fullName: entries[0].fullName,
    authorityIdentifiers: entries[0].authorityIdentifiers,
    roles: _join(
      entries.filter(({ role }) => role).map(({ role }) => role.title),
      ", "
    ),
  }));

  return (
    <>
      <List horizontal className="separated creators inline">
        {creators
          .slice(0, maxCreators)
          .map(({ fullName, authorityIdentifiers }) => (
            <List.Item
              as="span"
              className={`creatibutor-wrap separated ${className}`}
              key={fullName}
            >
              <CreatibutorSearchLink
                personName={fullName}
                searchUrl={searchUrl}
              />
              <CreatibutorIcons
                personName={fullName}
                identifiers={authorityIdentifiers}
              />
            </List.Item>
          ))}
      </List>
      {uniqueContributors.length > 0 && <DoubleSeparator />}
      <List horizontal className="separated contributors inline">
        {uniqueContributors.map(({ id, fullName, identifiers, roles }) => (
          <List.Item
            as="span"
            className={`creatibutor-wrap separated ${className}`}
            key={id}
          >
            <CreatibutorSearchLink
              personName={fullName}
              searchUrl={searchUrl}
              searchField="contributors"
            />
            <CreatibutorIcons personName={fullName} identifiers={identifiers} />
            {roles && <span className="contributor-role">({roles})</span>}
          </List.Item>
        ))}
      </List>
    </>
  );
}

ResultsItemCreatibutors.propTypes = {
  creators: PropTypes.array,
  contributors: PropTypes.array,
  maxCreators: PropTypes.number,
  maxContributors: PropTypes.number,
  searchUrl: PropTypes.string,
  className: PropTypes.string,
};
