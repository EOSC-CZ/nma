import React from "react";
import PropTypes from "prop-types";

import { Dropdown } from "semantic-ui-react";

const SortElement = ({
  currentSortBy,
  currentSortOrder,
  options,
  onValueChange,
  ariaLabel,
  selectOnNavigation,
}) => {
  const selected = currentSortOrder ? `${currentSortBy}-${currentSortOrder}` : currentSortBy;
  const _options = options.map((element, index) => {
    return {
      key: index,
      text: element.text,
      value: element.value,
    };
  });
  
  return (
    <Dropdown
      compact
      selection
      options={_options}
      value={selected}
      onChange={(e, { value }) => onValueChange(value)}
      aria-label={ariaLabel}
      selectOnNavigation={selectOnNavigation}
      className="sort-by-selector"
    />
  );
};

SortElement.propTypes = {
  options: PropTypes.array.isRequired,
  currentSortBy: PropTypes.string,
  currentSortOrder: PropTypes.string,
  ariaLabel: PropTypes.string,
  selectOnNavigation: PropTypes.bool,
  onValueChange: PropTypes.func.isRequired,
};

SortElement.defaultProps = {
  currentSortBy: null,
  currentSortOrder: null,
  ariaLabel: "Sort",
  selectOnNavigation: false,
};

export default SortElement;