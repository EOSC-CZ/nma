import React from "react";
import { Label } from "semantic-ui-react";
import PropTypes from "prop-types";

export const ResultsItemRights = ({ right }) => {
  const { rights, rightsURI } = right;
  return (
    <Label
      as="a"
      // href={`/vocabularies/access-rights/${rights}`} // TODO
      href={rightsURI}
      aria-label={rights}
      color="teal"
      size="small"
      className={rights}
    >
      {rights}
    </Label>
  );
};

ResultsItemRights.propTypes = {
  right: PropTypes.shape({
    rights: PropTypes.string.isRequired,
    rightsURI: PropTypes.string.isRequired,
  }),
};
