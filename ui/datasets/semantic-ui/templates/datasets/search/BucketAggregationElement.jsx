import React from "react";
import { Accordion } from "semantic-ui-react";

const BucketAggregationElement = ({ title, containerCmp, agg }) => {
  return (
    <div className="facets-item">
      <Accordion.Title as="a" className="accordion-title">
        <p>
          <span>{title}</span>
          <i className="chevron right icon facet-dropdown-caret"></i>
        </p>
      </Accordion.Title>
      <Accordion.Content className="facet-accordion-content">
        {containerCmp}
      </Accordion.Content>
    </div>
  );
};

export default BucketAggregationElement;
