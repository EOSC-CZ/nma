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
    searchFacet={`metadata_${searchField}_name`}
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
      key={`${i.nameIdentifierScheme}:${i.nameIdentifier}`}
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
      ({ name, nameIdentifiers = [] }) => {
        const idKeys = _join(
          nameIdentifiers.map((i) => `${i.nameIdentifierScheme}:${i.nameIdentifier}`),
          ";"
        );
        return `${name}-${idKeys}`;
      }
    )
  ).map(([groupKey, entries]) => ({
    id: groupKey,
    name: entries[0].name,
    nameIdentifiers: entries[0].nameIdentifiers,
    // roles: _join(
    //   entries.filter(({ role }) => role).map(({ role }) => role.title),
    //   ", "
    // ),
  }));

  const slicedCreators = creators.slice(0, maxCreators);
  
  return (
    <div className="ui double separated creatibutors">
      <List horizontal className="separated creators inline">
        {slicedCreators
          .map(({ name, nameIdentifiers }, index) => (
            <React.Fragment key={index}>
              <List.Item
                as="span"
                className={`creatibutor-wrap separated ${className}`}
              >
                <CreatibutorSearchLink
                  personName={name}
                  searchUrl={searchUrl}
                />
                <CreatibutorIcons
                  personName={name}
                  identifiers={nameIdentifiers}
                />
              </List.Item>
              {index < slicedCreators.length - 1 ? "; " : ""}
            </React.Fragment>
          ))}
      </List>
      {uniqueContributors.length > 0 && <DoubleSeparator />}
      <List horizontal className="separated contributors inline">
        {uniqueContributors.map(({ id, name, nameIdentifiers, roles }, index) => (
          <React.Fragment key={index} >
            <List.Item
              as="span"
              className={`creatibutor-wrap separated ${className}`}
              // TODO: id doesnt exist
            >
              <CreatibutorSearchLink
                personName={name}
                searchUrl={searchUrl}
                searchField="contributors"
              />
              <CreatibutorIcons personName={name} identifiers={nameIdentifiers} />
              {/* {roles && <span className="contributor-role">({roles})</span>} TODO: dont exist */}
            </List.Item>
            {index < uniqueContributors.length - 1 ? "; " : ""}
          </React.Fragment>
        ))}
      </List>
    </div>
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
