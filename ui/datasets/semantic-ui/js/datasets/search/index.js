import {
  parseSearchAppConfigs,
  createSearchAppsInit,
} from "@js/oarepo_ui/search";
import ResultsListItem from "./ResultsListItem";
import { SearchAppFacets } from "@js/oarepo_ui/search/SearchAppFacets";
import { parametrize } from "react-overridable";
import { SearchAppLayout } from "./SearchAppLayout";
import { ActiveFiltersElement } from "./ActiveFilters";
import { Dropdown } from "semantic-ui-react";
import { SearchAppResults } from "./SearchAppResults";

const [{ overridableIdPrefix }] = parseSearchAppConfigs();

const SearchAppFacetsWithProps = parametrize(SearchAppFacets, {
  allVersionsToggle: true,
});

const ResultsPerPage = ({ currentSize, options, onValueChange, ariaLabel, selectOnNavigation }) => {
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

const Sort = ({ options, currentSortBy, currentSortOrder, onValueChange, ariaLabel, selectOnNavigation }) => {
  const _options = options.map((element, index) => {
    return {
      key: index,
      text: element.text,
      value: element.value,
    };
  });
  const _computeValue = (sortBy, sortOrder) => {
    return sortOrder ? `${sortBy}-${sortOrder}` : sortBy;
  };
  const selected = _computeValue(currentSortBy, currentSortOrder);

  return (
    <Dropdown
      className="sort-by-selector"
      selection
      options={_options}
      value={selected}
      onChange={(e, { value }) => onValueChange(value)}
      aria-label={ariaLabel}
      selectOnNavigation={selectOnNavigation}
    />
  );
};

export const componentOverrides = {
  [`${overridableIdPrefix}.SearchApp.facets`]: SearchAppFacetsWithProps,
  [`${overridableIdPrefix}.ResultsList.item`]: ResultsListItem,
  [`${overridableIdPrefix}.SearchApp.layout`]: SearchAppLayout,
  [`${overridableIdPrefix}.ActiveFilters.element`]: ActiveFiltersElement,
  [`${overridableIdPrefix}.ResultsPerPage.element`]: ResultsPerPage,
  [`${overridableIdPrefix}.Sort.element`]: Sort,
  [`${overridableIdPrefix}.SearchApp.results`]: SearchAppResults,
};

createSearchAppsInit({ componentOverrides });