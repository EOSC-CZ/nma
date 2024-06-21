import PropTypes from "prop-types";
import React, { useContext } from "react";
import _groupBy from "lodash/groupBy";
import _map from "lodash/map";
import { Label, Icon, Grid } from "semantic-ui-react";
import { withState } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";
import _uniq from "lodash/merge";
import { i18next } from "@translations/i18next";
import { ClearFiltersButton } from "@js/oarepo_ui";

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
  ignoredFilters,
}) => {
  const searchAppContext = useContext(SearchConfigurationContext);
  const {
    initialQueryState: { filters: initialFilters },
  } = searchAppContext;

  const allFiltersToIgnore = _uniq([
    ...initialFilters.map((f) => f[0]),
    ...ignoredFilters,
  ]);

  const filtersWithoutInitialFilters = filters?.filter(
    (f) => !allFiltersToIgnore.includes(f[0])
  );
  const groupedData = _groupBy(filtersWithoutInitialFilters, 0);
  return (
    <Grid padded relaxed>
      <Grid.Column only="computer">
        <div className="flex wrap align-items-center">
          {_map(groupedData, (filters, key) => (
            <span key={key} className="active-filters-labels">
              {aggregations[key]?.label &&
                <Label pointing="right">
                  <Icon name="filter" />
                  {aggregations[key]?.label}
                </Label>
              }
              {filters.map((filter, index) => {
                const { label, activeFilter } = getLabel(filter, aggregations);
                return (
                  <Label
                    color="pink"
                    key={activeFilter}
                    onClick={() => removeActiveFilter(activeFilter)}
                    type="button"
                    tabIndex="0"
                    aria-label={`${i18next.t("Remove filter")} ${label}`}
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
              })}
            </span>
          ))}
          <ClearFiltersButton ignoredFilters={ignoredFilters} clearFiltersButtonClassName="primary" />
        </div>
      </Grid.Column>
    </Grid>
  );
};

const ActiveFiltersElement = withState(ActiveFiltersElementComponent);

export default ActiveFiltersElement;

ActiveFiltersElementComponent.propTypes = {
  filters: PropTypes.array,
  ignoredFilters: PropTypes.array,
  removeActiveFilter: PropTypes.func.isRequired,
  getLabel: PropTypes.func.isRequired,
  currentResultsState: PropTypes.shape({
    data: PropTypes.shape({
      aggregations: PropTypes.object,
    }).isRequired,
  }).isRequired,
};

ActiveFiltersElementComponent.defaultProps = { ignoredFilters: [] };
