import React, { useState } from "react";
import PropTypes from "prop-types";
import { Dropdown } from "semantic-ui-react";

const ResultsPerPageElement = ({
  currentSize,
  options,
  onValueChange,
  ariaLabel,
  selectOnNavigation,
}) => {
  const _options = options.map((element, index) => {
    return { key: index, text: element.text, value: element.value };
  });

  const [open, setOpen] = useState(false);

  return (
    <Dropdown
      compact
      selection
      open={open}
      onOpen={() => setOpen(true)}
      onClose={() => setOpen(false)}
      options={_options}
      value={currentSize}
      onChange={(e, { value }) => onValueChange(value)}
      aria-label={ariaLabel}
      selectOnNavigation={selectOnNavigation}
      className="results-per-page-selector"
    />
  );
};

Element.propTypes = {
  currentSize: PropTypes.number.isRequired,
  options: PropTypes.array.isRequired,
  ariaLabel: PropTypes.string,
  selectOnNavigation: PropTypes.bool,
  onValueChange: PropTypes.func.isRequired,
};

export default ResultsPerPageElement;
