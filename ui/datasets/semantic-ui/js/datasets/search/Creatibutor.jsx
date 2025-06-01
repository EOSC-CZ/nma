import React from "react";
import PropTypes from "prop-types";
import { IdentifierBadge } from "@js/oarepo_ui/components/IdentifierBadge";

const formatName = (person) => {
  const lastName = person.family_name || "";
  const givenNames = person.given_names || [];

  if (givenNames.length === 0) {
    return lastName;
  }

  const formattedGivenNames = givenNames.join(" ");

  return `${lastName}, ${formattedGivenNames}`;
};

export const Creatibutor = ({ creatibutor }) => {
  const isPerson = !!creatibutor.person;
  const role = creatibutor?.role?.labels?.[0]?.value;
  let identifiers = isPerson
    ? creatibutor?.person.external_identifiers?.map((identifier) => ({
        scheme: identifier.identifier_scheme,
        identifier: identifier.value,
        url: identifier.iri,
      }))
    : creatibutor?.organization.external_identifiers?.map((identifier) => ({
        scheme: identifier.identifier_scheme,
        identifier: identifier.value,
        url: identifier.iri,
      }));

  //TODO: Hacky way to handle the identifiers, but as the schemes are various,
  // it is difficult to reuse existing component. We can remove when https://linear.app/ducesnet/issue/FE-373/identifiers
  // is implemented
  identifiers = identifiers?.map((identifier) => {
    const scheme = identifier.scheme?.toLowerCase() || "";

    if (scheme?.includes("orcid")) {
      return {
        ...identifier,
        scheme: "orcid",
      };
    }

    if (scheme?.includes("ror")) {
      return {
        ...identifier,
        scheme: "ror",
      };
    }

    return identifier;
  });

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
      {role && `( ${role} )`}
    </span>
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

export default Creatibutor;
