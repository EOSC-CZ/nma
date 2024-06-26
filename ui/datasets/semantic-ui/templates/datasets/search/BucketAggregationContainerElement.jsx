import React from "react";
import { List } from "semantic-ui-react";

const BucketAggregationContainerElement = ({ valuesCmp }) => {
  return (
    <List relaxed>{valuesCmp}</List>
  );
};

export default BucketAggregationContainerElement;
