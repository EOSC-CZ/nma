import {
  createSearchAppsInit,
  parseSearchAppConfigs,
  SearchappSearchbarElement,
} from "@js/oarepo_ui";

const [searchAppConfig, ..._] = parseSearchAppConfigs();
const { overridableIdPrefix } = searchAppConfig;

export * from "./components";

export const componentOverrides = {
  [`${overridableIdPrefix}.SearchBar.element`]: SearchappSearchbarElement,
};

createSearchAppsInit({ componentOverrides });
