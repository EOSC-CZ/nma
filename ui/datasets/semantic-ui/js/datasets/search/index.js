import {
  parseSearchAppConfigs,
  createSearchAppsInit,
} from "@js/oarepo_ui/search";

import {
  RDMCountComponent,
  RDMEmptyResults,
  RDMErrorComponent,
  RDMRecordResultsGridItem,
  RDMRecordSearchBarContainer,
  RDMRecordMultipleSearchBarElement,
  RDMToggleComponent,
} from "@js/invenio_app_rdm/search/components";
import {
  ContribSearchAppFacets,
  ContribBucketAggregationElement,
  ContribBucketAggregationValuesElement,
} from "@js/invenio_search_ui/components";
import { parametrize } from "react-overridable";

import ResultsListItem from "./ResultsListItem";

const [{ overridableIdPrefix }] = parseSearchAppConfigs();

export const RDMRecordSearchBarContainerWithConfig = parametrize(RDMRecordSearchBarContainer, {
  appName: overridableIdPrefix,
});

export const componentOverrides = {
  [`${overridableIdPrefix}.BucketAggregation.element`]: ContribBucketAggregationElement,
  [`${overridableIdPrefix}.BucketAggregationValues.element`]: ContribBucketAggregationValuesElement,
  [`${overridableIdPrefix}.ResultsGrid.item`]: RDMRecordResultsGridItem,
  [`${overridableIdPrefix}.EmptyResults.element`]: RDMEmptyResults,
  [`${overridableIdPrefix}.ResultsList.item`]: ResultsListItem,
  [`${overridableIdPrefix}.SearchApp.facets`]: ContribSearchAppFacets,
  [`${overridableIdPrefix}.SearchApp.searchbarContainer`]: RDMRecordSearchBarContainerWithConfig,
  [`${overridableIdPrefix}.SearchBar.element`]: RDMRecordMultipleSearchBarElement,
  [`${overridableIdPrefix}.Count.element`]: RDMCountComponent,
  [`${overridableIdPrefix}.Error.element`]: RDMErrorComponent,
  [`${overridableIdPrefix}.SearchFilters.Toggle.element`]: RDMToggleComponent,
};

createSearchAppsInit({ componentOverrides });
