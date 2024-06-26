import PropTypes from "prop-types";
import React from "react";
import { Item } from "semantic-ui-react";

const ResultsListContainer = ({ children }) => {
  return (
    <Item.Group relaxed link className="search-listing-item-group">
      {children}
    </Item.Group>
  );
};

ResultsListContainer.propTypes = {
  children: PropTypes.array.isRequired,
};

export default ResultsListContainer;
