import React from "react";
import PropTypes from "prop-types";
import { IdentifierBadge } from "@js/oarepo_ui/components/IdentifierBadge";

const formatName = (person) => {
  const familyName = person.family_name;
  const givenName = person.given_name;
  if (familyName && givenName) {
    return `${familyName}, ${givenName}`;
  }
  return person.name || familyName || givenName || "";
};

const normalizeIdentifier = (identifier) => {
  const scheme =
    (identifier?.scheme || identifier?.identifier_scheme?.id || "").toLowerCase();
  const value = identifier?.identifier || identifier?.value;

  let url = identifier?.url;
  if (!url && typeof value === "string" && value.startsWith("http")) {
    url = value;
  } else if (!url && scheme === "orcid") {
    url = `https://orcid.org/${value}`;
  } else if (!url && scheme === "ror") {
    url = `https://ror.org/${value}`;
  }

  return {
    scheme: scheme || undefined,
    identifier: value,
    url,
  };
};

export const Creatibutor = ({ creatibutor }) => {
  const personOrOrg = creatibutor.person_or_org || creatibutor.person || creatibutor.organization;
  const isPerson = (personOrOrg?.type || "personal") !== "organizational";
  const identifiers = Array.isArray(personOrOrg?.identifiers)
    ? personOrOrg.identifiers.map(normalizeIdentifier)
    : [];

  const selectedIdentifier =
    Array.isArray(identifiers) && identifiers.length > 0
      ?
        identifiers.find((identifier) => {
          const schemeLower = identifier?.scheme?.toLowerCase();
          return schemeLower === "orcid" || schemeLower === "ror";
        }) || identifiers[0]
      : null;

  const name = isPerson ? formatName(personOrOrg || {}) : personOrOrg?.name;
  const role =
    typeof creatibutor?.role?.title === "string"
      ? creatibutor.role.title
      : (creatibutor?.role?.title?.["en"] ||
         creatibutor?.role?.title?.["cs"] ||
         creatibutor?.role?.title_l10n ||
         creatibutor?.role?.id);

  return (
    <span className="mb-5 mr-0 inline-block">
      {`${name}`}
      {selectedIdentifier && (
        <React.Fragment>
          {" "}
          <IdentifierBadge
            identifier={selectedIdentifier}
            creatibutorName={name}
            className="mr-0"
          />
        </React.Fragment>
      )}
      {role && role.toLowerCase() !== "creator" && (
        <span className="creatibutor-role">{` (${role})`}</span>
      )}
    </span>
  );
};

Creatibutor.propTypes = {
  creatibutor: PropTypes.shape({
    person_or_org: PropTypes.shape({
      type: PropTypes.string,
      name: PropTypes.string,
      given_name: PropTypes.string,
      family_name: PropTypes.string,
      identifiers: PropTypes.array,
    }),
    role: PropTypes.shape({
      id: PropTypes.string,
      title: PropTypes.oneOfType([PropTypes.object, PropTypes.string]),
      title_l10n: PropTypes.string,
    }),
  }).isRequired,
};

export default Creatibutor;
