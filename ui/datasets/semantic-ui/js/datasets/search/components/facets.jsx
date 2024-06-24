import { i18next } from "@translations/invenio_search_ui/i18next";
import React, { useState } from "react";
import {
  Accordion,
  Button,
  Checkbox,
  List,
} from "semantic-ui-react";
import PropTypes from "prop-types";

export const ContribParentFacetValue = ({
  bucket,
  keyField,
  isSelected,
  childAggCmps,
  onFilterClicked,
}) => {
  const [isActive, setIsActive] = useState(false);

  return (
    <Accordion>
      <Accordion.Title
        onClick={() => {}}
        key={`panel-${bucket.label}`}
        active={isActive}
        className="facet-wrapper parent"
      >
        <List.Content className="facet-wrapper">
          <Button
            icon="angle right"
            className="transparent"
            onClick={() => setIsActive(!isActive)}
            aria-label={
              i18next.t("Show all sub facets of ") + bucket.label || keyField
            }
          />
          <Checkbox
            label={bucket.label || keyField}
            id={`${keyField}-facet-checkbox`}
            aria-describedby={`${keyField}-count`}
            value={keyField}
            checked={isSelected}
            onClick={() => onFilterClicked(keyField)}
          />
          {" "}
          <span id={`${keyField}-count`} className="facet-count">
            ({bucket.doc_count})
          </span>
        </List.Content>
      </Accordion.Title>
      <Accordion.Content active={isActive}>{childAggCmps}</Accordion.Content>
    </Accordion>
  );
};

ContribParentFacetValue.propTypes = {
  bucket: PropTypes.object.isRequired,
  keyField: PropTypes.string.isRequired,
  isSelected: PropTypes.bool.isRequired,
  childAggCmps: PropTypes.node.isRequired,
  onFilterClicked: PropTypes.func.isRequired,
};

export const ContribFacetValue = ({
  bucket,
  keyField,
  isSelected,
  onFilterClicked,
}) => {
  const keyFieldTokens = keyField.split("____");
  let filterKey;
  switch (keyFieldTokens.length) {
    case 0:
      filterKey = keyField;
      break;
    case 1:
      filterKey = keyFieldTokens[0];
      break;
    case 2:
      filterKey = keyFieldTokens[1];
      break;
    default:
      filterKey = keyFieldTokens.slice(1).join("____");
  }

  return (
    <List.Content className="facet-value-element">
      <Checkbox
        className="facet-checkbox"
        onClick={() => onFilterClicked(filterKey)}
        label={bucket.label || keyField}
        id={`${keyField}-facet-checkbox`}
        aria-describedby={`${keyField}-count`}
        value={keyField}
        checked={isSelected}
      />
      {" "}
      <span id={`${keyField}-count`} className="facet-count">
        ({bucket.doc_count})
      </span>
    </List.Content>
  );
};

ContribFacetValue.propTypes = {
  bucket: PropTypes.object.isRequired,
  keyField: PropTypes.string.isRequired,
  isSelected: PropTypes.bool.isRequired,
  onFilterClicked: PropTypes.func.isRequired,
};

export const ContribBucketAggregationValuesElement = ({
  bucket,
  isSelected,
  onFilterClicked,
  childAggCmps,
}) => {
  const hasChildren = childAggCmps && childAggCmps.props.buckets.length > 0;
  const keyField = bucket.key_as_string ? bucket.key_as_string : bucket.key;
  console.log(bucket, hasChildren);
  return (
    <List.Item key={bucket.key}>
      {hasChildren ? (
        <ContribParentFacetValue
          bucket={bucket}
          keyField={keyField}
          isSelected={isSelected}
          childAggCmps={childAggCmps}
          onFilterClicked={onFilterClicked}
        />
      ) : (
        <ContribFacetValue
          bucket={bucket}
          keyField={keyField}
          isSelected={isSelected}
          onFilterClicked={onFilterClicked}
        />
      )}
    </List.Item>
  );
};

ContribBucketAggregationValuesElement.propTypes = {
  bucket: PropTypes.object.isRequired,
  childAggCmps: PropTypes.node,
  isSelected: PropTypes.bool.isRequired,
  onFilterClicked: PropTypes.func.isRequired,
};

ContribBucketAggregationValuesElement.defaultProps = {
  childAggCmps: null,
};

