import React from "react";
import { Dropdown } from "semantic-ui-react";

export const ResultsPerPageElement = ({ currentSize, options, onValueChange, ariaLabel, selectOnNavigation }) => {
  const _options = options.map((element, index) => {
    return { key: index, text: element.text, value: element.value };
  });
  return (
    <Dropdown
      className="results-per-page-selector"
      selection
      compact
      options={_options}
      value={currentSize}
      onChange={(e, { value }) => onValueChange(value)}
      aria-label={ariaLabel}
      selectOnNavigation={selectOnNavigation}
    />
  );
};
