import React from "react";
import { Image } from "semantic-ui-react";
import PropTypes from "prop-types";

const iconsObject = {
  c_abf2: "zamky_open_access.svg",
  c_16ec: "zamky_Partialy_closed_access.svg",
  c_f1cf: "zamky_Closed_access.svg",
  c_14cb: "zamky_Partialy_closed_access.svg",
};

export const ResultsItemAccessStatus = ({ status }) => {
  const { id, title } = status;
  const iconFile = iconsObject[id] || null;
  return (
    iconFile && (
      <Image
        as="a"
        href={`/vocabularies/access-rights/${id}`}
        centered
        fluid
        title={title}
        aria-label={title}
        className={`access-status ${title}`}
        src={`/static/icons/locks/${iconFile}`}
      />
    )
  );
};

ResultsItemAccessStatus.propTypes = {
  status: PropTypes.shape({
    id: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
  }),
};
