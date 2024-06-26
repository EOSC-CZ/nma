import React from "react";
import { BucketAggregation } from "react-searchkit";
import { Accordion } from "semantic-ui-react";
import $ from "jquery";

const initAccordion = () => {
  $(".ui.accordion").accordion({
    exclusive: false,
  });
};

const SearchAppFacets = ({ aggs }) => {

  React.useEffect(initAccordion, []);

  return (
    <div className="facets-container">
      <div className="facet-list">
        <Accordion exclusive={false} className="facets-accordion">
          {aggs.map((agg) => (
            <BucketAggregation
              key={agg.aggName}
              title={agg.title}
              agg={agg}
            />
          ))}
        </Accordion>
      </div>
    </div>
  );
};

export default SearchAppFacets;
