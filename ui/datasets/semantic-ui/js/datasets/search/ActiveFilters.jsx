import PropTypes from "prop-types";
import React from "react";
import _groupBy from "lodash/groupBy";
import _map from "lodash/map";
import { Label, Icon } from "semantic-ui-react";
import { withState } from "react-searchkit";
import { ClearFiltersButton } from "@js/oarepo_ui";
import { useActiveSearchFilters } from "@js/oarepo_ui/search/hooks";
import { i18next } from "@translations/i18next";

const getLabel = (filter, aggregations) => {
  const aggName = filter[0];
  let value = filter[1];
  const label =
    aggregations[aggName]?.buckets?.find((b) => b.key === value)?.label ||
    value;
  let currentFilter = [aggName, value];
  const hasChild = filter.length === 3;
  if (hasChild) {
    const { label, activeFilter } = getLabel(filter[2]);
    value = `${value}.${label}`;
    currentFilter.push(activeFilter);
  }
  return {
    label: label,
    activeFilter: currentFilter,
  };
};
const ActiveFiltersElementComponent = ({
  filters,
  removeActiveFilter,
  currentResultsState: {
    data: { aggregations },
  },
}) => {
  const activeFilters = useActiveSearchFilters(filters);
  const groupedData = _groupBy(activeFilters, 0);
  return (
    <>
      {_map(groupedData, (filters, key) =>
        filters.map((filter, index) => {
          const { label, activeFilter } = getLabel(filter, aggregations);
          return (
            <Label
              className="active-filter-label mb-5"
              key={activeFilter}
              onClick={() => removeActiveFilter(activeFilter)}
              type="button"
              tabIndex="0"
              aria-label={`Remove filter ${label}`}
              onKeyPress={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  removeActiveFilter(activeFilter);
                }
              }}
            >
              {label}
              <Icon name="delete" aria-hidden="true" />
            </Label>
          );
        })
      )}
      <ClearFiltersButton
        content={i18next.t("Clear all")}
        icon={null}
        labelPosition={null}
        size="medium"
      />
    </>
  );
};

export const ActiveFiltersElement = withState(ActiveFiltersElementComponent);

ActiveFiltersElementComponent.propTypes = {
  filters: PropTypes.array,
  removeActiveFilter: PropTypes.func.isRequired,
  currentResultsState: PropTypes.shape({
    data: PropTypes.shape({
      aggregations: PropTypes.object,
    }).isRequired,
  }).isRequired,
};
