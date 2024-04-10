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
      inline
      icon={open ? "caret up" : "caret down"}
      open={open}
      onOpen={() => setOpen(true)}
      onClose={() => setOpen(false)}
      options={_options}
      value={currentSize}
      onChange={(e, { value }) => onValueChange(1)}
      aria-label={ariaLabel}
      selectOnNavigation={selectOnNavigation}
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
