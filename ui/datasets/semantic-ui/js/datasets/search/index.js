import React from "react";
import PropTypes from "prop-types";
import {
  parseSearchAppConfigs,
  createSearchAppsInit,
  SearchappSearchbarElement,
} from "@js/oarepo_ui/search";
import ResultsListItem from "./ResultsListItem";
import { SearchAppFacets } from "@js/oarepo_ui/search/SearchAppFacets";
import { parametrize } from "react-overridable";
import { SearchAppLayout } from "./SearchAppLayout";
import { ActiveFiltersElement } from "./ActiveFilters";
import { Dropdown } from "semantic-ui-react";
import { SearchAppResults } from "./SearchAppResults";
import { i18next } from "@translations/i18next";

const SearchAppFacetsWithProps = parametrize(SearchAppFacets, {
  allVersionsToggle: true,
});

const SearchappSearchbarElementWithProps = parametrize(
  SearchappSearchbarElement,
  {
    actionProps: { content: i18next.t("Search"), icon: null },
    placeholder: i18next.t("Search datasets.."),
  }
);

const ResultsPerPage = ({
  currentSize,
  options,
  onValueChange,
  ariaLabel,
  selectOnNavigation,
}) => {
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

ResultsPerPage.propTypes = {
  currentSize: PropTypes.number.isRequired,
  options: PropTypes.array.isRequired,
  onValueChange: PropTypes.func.isRequired,
  ariaLabel: PropTypes.string,
  selectOnNavigation: PropTypes.bool,
};

const Sort = ({
  options,
  currentSortBy,
  currentSortOrder,
  onValueChange,
  ariaLabel,
  selectOnNavigation,
}) => {
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

Sort.propTypes = {
  options: PropTypes.array.isRequired,
  currentSortBy: PropTypes.string,
  currentSortOrder: PropTypes.string,
  onValueChange: PropTypes.func.isRequired,
  ariaLabel: PropTypes.string,
  selectOnNavigation: PropTypes.bool,
};
/** NOTE: This reads configs for any search app present on a page
 *   In HTML/Jinja, a single search app instance is typically represented
 */
const [{ overridableIdPrefix }] = parseSearchAppConfigs();

/** NOTE: To customize components in a specific search app instance,
 *   you need to obtain its `overridableIdPrefix` from the corresponding config first
 */

export const componentOverrides = {
  /** NOTE: Then you can then replace any existing search ui
   * component with your own implementation, e.g.:
   */
  [`${overridableIdPrefix}.SearchApp.facets`]: SearchAppFacetsWithProps,
  [`${overridableIdPrefix}.ResultsList.item`]: ResultsListItem,
  [`${overridableIdPrefix}.SearchApp.layout`]: SearchAppLayout,
  [`${overridableIdPrefix}.ActiveFilters.element`]: ActiveFiltersElement,
  [`${overridableIdPrefix}.SearchBar.element`]:
    SearchappSearchbarElementWithProps,
  [`${overridableIdPrefix}.ResultsPerPage.element`]: ResultsPerPage,
  [`${overridableIdPrefix}.Sort.element`]: Sort,
  [`${overridableIdPrefix}.SearchApp.results`]: SearchAppResults,
};

createSearchAppsInit({ componentOverrides });
