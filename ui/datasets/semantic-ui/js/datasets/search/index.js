import {
  parseSearchAppConfigs,
  createSearchAppsInit,
} from "@js/oarepo_ui/search";
import {
  RDMCountComponent,
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
import { EmptyResultsElement } from "./EmptyResultsElement";
import ResultsListItem from "./ResultsListItem";

const [{ overridableIdPrefix }] = parseSearchAppConfigs();

export const RDMRecordSearchBarContainerWithConfig = parametrize(
  RDMRecordSearchBarContainer,
  {
    appName: overridableIdPrefix,
  }
);

const ContribSearchAppFacetsWithConfig = parametrize(ContribSearchAppFacets, {
  toggle: false,
});


export const componentOverrides = {
  [`${overridableIdPrefix}.ResultsGrid.item`]: RDMRecordResultsGridItem,
  [`${overridableIdPrefix}.EmptyResults.element`]: EmptyResultsElement,
  [`${overridableIdPrefix}.ResultsList.item`]: ResultsListItem,
  [`${overridableIdPrefix}.SearchApp.searchbarContainer`]:
    RDMRecordSearchBarContainerWithConfig,
  [`${overridableIdPrefix}.SearchBar.element`]:
    RDMRecordMultipleSearchBarElement,
  [`${overridableIdPrefix}.Count.element`]: RDMCountComponent,
  [`${overridableIdPrefix}.Error.element`]: RDMErrorComponent,
  [`${overridableIdPrefix}.SearchFilters.Toggle.element`]: RDMToggleComponent,
  [`${overridableIdPrefix}.BucketAggregation.element`]: ContribBucketAggregationElement,
  [`${overridableIdPrefix}.BucketAggregationValues.element`]: ContribBucketAggregationValuesElement,
  [`${overridableIdPrefix}.SearchApp.facets`]: ContribSearchAppFacetsWithConfig,
};
console.log({componentOverrides})
createSearchAppsInit({ componentOverrides });
