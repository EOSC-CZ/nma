import React from "react";
import { Container } from "semantic-ui-react";
import { BaseFormLayout } from "@js/oarepo_ui";
import { FormValidationSchema } from "./FormValidationSchema";

export const FormAppLayout = () => {
  const formikProps = {
    validationSchema: FormValidationSchema,
  };
  return (
    <Container fluid>
      <BaseFormLayout formikProps={formikProps} />
    </Container>
  );
};
export default FormAppLayout;
