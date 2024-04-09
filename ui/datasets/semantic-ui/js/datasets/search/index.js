import {
  createSearchAppsInit,
  parseSearchAppConfigs,
} from "@js/oarepo_ui";

const [searchAppConfig, ..._] = parseSearchAppConfigs();
const { overridableIdPrefix } = searchAppConfig;

export * from "./components";

export const componentOverrides = {};

createSearchAppsInit({ componentOverrides });
