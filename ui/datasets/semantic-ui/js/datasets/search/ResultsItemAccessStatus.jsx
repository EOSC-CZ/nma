import React from "react";
import PropTypes from "prop-types";

export const ResultsItemAccessStatus = ({ status }) => {
  const { id, title } = status || {};

  const idToLockIcons = {
    c_abf2: "open_access.svg",
    c_16ec: "partialy_closed_access_grey.svg",
    c_f1cf: "closed_access.svg",
    c_14cb: "partialy_closed_access.svg",
  };

  if (!id || !idToLockIcons[id]) {
    return null;
  }

  return (
    <a
      href={`/vocabularies/access-rights/${id}`}
      className="access-rights-link"
    >
      <img
        className="ui tiny middle aligned image license-rights"
        src={`/static/icons/locks/${idToLockIcons[id]}`}
        title={title}
        alt={title}
        aria-label={title}
      />
    </a>
  );
};

ResultsItemAccessStatus.propTypes = {
  status: PropTypes.shape({
    id: PropTypes.string,
    title: PropTypes.string,
  }),
};

export default ResultsItemAccessStatus;
