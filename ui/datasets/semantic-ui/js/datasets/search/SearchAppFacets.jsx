import { SearchAppFacets as OArepoUISearchAppFacets } from "@js/oarepo_ui/search/SearchAppFacets";
import { parametrize } from "react-overridable";

export const SearchAppFacets = parametrize(OArepoUISearchAppFacets, {
  allVersionsToggle: false,
});
