import React from "react";
import { Image } from "semantic-ui-react";
import PropTypes from "prop-types";

export const ResultsItemLicense = ({ rights }) => {
  const badge = rights?.id === "3-BY-ND-CZ" ? "by-nd.png" : null;
  const { id, title } = rights;

  return badge ? (
    <Image
      as="a"
      href={`/vocabularies/licenses/${id}`}
      key={id}
      centered
      fluid
      className="license-rights"
      src={`/static/images/licenses/${badge}`}
      title={title}
      aria-label={title}
    />
  ) : null;
};

ResultsItemLicense.propTypes = {
  rights: PropTypes.object,
};
