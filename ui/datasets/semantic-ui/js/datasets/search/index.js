import {
  parseSearchAppConfigs,
  createSearchAppsInit,
} from "@js/oarepo_ui/search";

import ResultsListItem from "./ResultsListItem";
import { SearchAppLayout } from "./SearchAppLayout";
import { ActiveFiltersElement } from "./ActiveFiltersElement";
import { SearchAppResults } from "./SearchAppResults";
import { SortElement } from "./SortElement";
import { ResultsPerPageElement } from "./ResultsPerPageElement";
// import { SearchAppFacets } from "./SearchAppFacets";
import { EmptyResultsElement } from "./EmptyResultsElement";

const [{ overridableIdPrefix }] = parseSearchAppConfigs();

export const componentOverrides = {
  // [`${overridableIdPrefix}.SearchApp.facets`]: SearchAppFacets,
  [`${overridableIdPrefix}.ResultsList.item`]: ResultsListItem,
  [`${overridableIdPrefix}.SearchApp.layout`]: SearchAppLayout,
  [`${overridableIdPrefix}.ActiveFilters.element`]: ActiveFiltersElement,
  [`${overridableIdPrefix}.ResultsPerPage.element`]: ResultsPerPageElement,
  [`${overridableIdPrefix}.Sort.element`]: SortElement,
  [`${overridableIdPrefix}.SearchApp.results`]: SearchAppResults,
  [`${overridableIdPrefix}.EmptyResults.element`]: EmptyResultsElement,
};

createSearchAppsInit({ componentOverrides });