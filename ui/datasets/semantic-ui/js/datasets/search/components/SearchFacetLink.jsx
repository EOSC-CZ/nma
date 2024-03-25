import React from "react";
import PropTypes from "prop-types";

export const SearchFacetLink = ({
  searchUrl = "/",
  searchFacet,
  value,
  title,
  label,
  className,
  ...rest
}) => (
  <a
    className={`${className} ui search-link`}
    href={`${searchUrl}?q=&f=${searchFacet}:${encodeURI(value)}`}
    aria-label={title}
    title={title}
    {...rest}
  >
    <span className={`${className} label`}>{label || value}</span>
  </a>
);

SearchFacetLink.propTypes = {
  searchUrl: PropTypes.string,
  searchFacet: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  title: PropTypes.string,
  label: PropTypes.string,
  className: PropTypes.string,
};
