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
};

createSearchAppsInit({ componentOverrides });
