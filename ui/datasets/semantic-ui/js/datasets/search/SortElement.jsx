import React from "react";
import { Dropdown } from "semantic-ui-react";

export const SortElement = ({ options, currentSortBy, currentSortOrder, onValueChange, ariaLabel, selectOnNavigation }) => {
  const _options = options.map((element, index) => {
    return {
      key: index,
      text: element.text,
      value: element.value,
    };
  });
  const _computeValue = (sortBy, sortOrder) => {
    return sortOrder ? `${sortBy}-${sortOrder}` : sortBy;
  };
  const selected = _computeValue(currentSortBy, currentSortOrder);

  return (
    <Dropdown
      className="sort-by-selector"
      selection
      options={_options}
      value={selected}
      onChange={(e, { value }) => onValueChange(value)}
      aria-label={ariaLabel}
      selectOnNavigation={selectOnNavigation}
    />
  );
};
