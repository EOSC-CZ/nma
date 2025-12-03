import { DepositFormApp, parseFormAppConfig } from "@js/oarepo_ui/forms";
import React from "react";
import ReactDOM from "react-dom";
import { OARepoDepositSerializer } from "@js/oarepo_ui/api";
import FormFieldsContainer from "./FormFieldsContainer";
import { BaseFormLayout } from "./BaseFormLayout";
import { DepositBootstrap } from "@js/invenio_rdm_records/src/deposit/api/DepositBootstrap";
import { Container } from "semantic-ui-react";
const recordSerializer = new OARepoDepositSerializer(
  ["errors", "expanded"],
  ["__key"]
);

const { rootEl, config, ...rest } = parseFormAppConfig();

const overridableIdPrefix = config.overridableIdPrefix;

const FormLayout = () => (
  <Container className="rel-mt-1">
    <DepositBootstrap>
      <BaseFormLayout />
    </DepositBootstrap>
  </Container>
);

export const componentOverrides = {
  [`${overridableIdPrefix}.FormApp.layout`]: FormLayout,
};

ReactDOM.render(
  <DepositFormApp
    config={config}
    {...rest}
    recordSerializer={recordSerializer}
    componentOverrides={componentOverrides}
  />,
  rootEl
);
