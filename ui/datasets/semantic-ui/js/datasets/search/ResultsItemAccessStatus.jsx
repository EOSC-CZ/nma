import React from "react";
import PropTypes from "prop-types";
import { Label, Icon } from "semantic-ui-react";

const idToLockIcons = {
  open: "open_access.svg",
  public: "open_access.svg",
  "metadata-only": "partially_closed_access_grey.svg",
  restricted: "partially_closed_access.svg",
  embargoed: "partially_closed_access_grey.svg",
  closed: "closed_access.svg",
};

const idToTitle = {
  open: "Open access",
  public: "Open access",
  "metadata-only": "Metadata only",
  restricted: "Restricted access",
  embargoed: "Embargoed",
  closed: "Closed access",
};

const normalizeStatus = (status) => {
  if (!status) return null;

  const pickId = (value) => {
    if (!value) return null;
    const id = typeof value === "string" ? value : value.id || value.status || value.record || value.files;
    return id || null;
  };

  const rawId = pickId(status);
  if (!rawId) return null;

  const normalizedId = rawId.toLowerCase();

  return {
    id: normalizedId,
    title: status.title || status.title_l10n || status.description_l10n || idToTitle[normalizedId] || normalizedId,
  };
};

export const ResultsItemAccessStatus = ({ status }) => {
  const normalized = normalizeStatus(status);

  if (!normalized) {
    return null;
  }

  const { id, title } = normalized;
  const iconName = idToLockIcons[id];

  if (!iconName) {
    return (
      <Label basic size="small">
        <Icon name="lock" />
        {title || id}
      </Label>
    );
  }

  return (
    <a href={`/vocabularies/access-rights/${id}`} className="access-rights-link">
      <img
        className="ui tiny middle aligned image license-rights"
        src={`/static/icons/locks/${iconName}`}
        title={title}
        alt={title}
        aria-label={title}
      />
    </a>
  );
};

ResultsItemAccessStatus.propTypes = {
  status: PropTypes.oneOfType([
    PropTypes.shape({
      id: PropTypes.string,
      status: PropTypes.string,
      record: PropTypes.string,
      files: PropTypes.string,
      title: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
      title_l10n: PropTypes.string,
      description_l10n: PropTypes.string,
    }),
    PropTypes.string,
  ]),
};

export default ResultsItemAccessStatus;
