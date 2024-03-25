import React from "react";
import { i18next } from "@translations/i18next";
import PropTypes from "prop-types";

export const IconIdentifier = ({ link, linkTitle, icon, alt }) => {
  return (
    <a
      className="no-text-decoration mr-0"
      href={link}
      aria-label={linkTitle}
      title={linkTitle}
      key={link}
    >
      <img className="inline-id-icon ml-5" src={icon} alt={alt} />
    </a>
  );
};

IconIdentifier.propTypes = {
  link: PropTypes.string,
  linkTitle: PropTypes.string,
  icon: PropTypes.string,
  alt: PropTypes.string,
};

export const IconPersonIdentifier = ({ identifier, personName }) => {
  const { nameIdentifierScheme: scheme, nameIdentifier: value } = identifier;
  let link = null;
  let linkTitle = null;
  let icon = null;
  let alt = "";

  // TODO: implement these cases
  // "czenasAutID",
  // "vedidk",
  // "institutionalID",
  // "ISNI",
  // "ICO",

  switch (scheme.toLowerCase()) {
    case "orcid":
      return (
        <IconIdentifier
          link={value}
          linkTitle={`${personName}: ${i18next.t("ORCID profile")}`}
          icon="/static/images/identifiers/orcid-og-image.png"
          alt="ORCID logo"
        />
      );
    case "scopusid":
      return (
        <IconIdentifier
          link={value}
          linkTitle={`${personName}: ${i18next.t("Scopus ID profile")}`}
          icon="/static/images/scopus.svg"
          alt="ScopusID logo"
        />
      );
    case "ror":
      return (
        <IconIdentifier
          link={value}
          linkTitle={`${personName}: ${i18next.t("ROR profile")}`}
          //   TODO: add correct icon
          icon="/static/images/orcid.png"
          alt="ROR logo"
        />
      );
    case "researcherid":
      return (
        <IconIdentifier
          link={value}
          linkTitle={`${personName}: ${i18next.t("WOS Researcher ID")}`}
          //   TODO: add correct icon
          icon="/static/images/orcid.png"
          alt="WOS Researcher ID logo"
        />
      );
    case "doi":
      return (
        <IconIdentifier
          link={value}
          linkTitle={`${personName}: ${i18next.t("DOI profile")}`}
          //   TODO: add correct icon
          icon="/static/images/orcid.png"
          alt="DOI logo"
        />
      );
    case "gnd":
      return (
        <IconIdentifier
          link={value}
          linkTitle={`${personName}: ${i18next.t("GND profile")}`}
          //   TODO: add correct icon
          icon="/static/images/orcid.png"
          alt="GND logo"
        />
      );
    default:
      return null;
  }
};

IconPersonIdentifier.propTypes = {
  identifier: PropTypes.shape({
    identifierScheme: PropTypes.string,
    nameIdentifier: PropTypes.string,
  }),
  personName: PropTypes.string,
};
