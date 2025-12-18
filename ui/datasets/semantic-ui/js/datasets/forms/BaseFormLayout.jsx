import React, { useEffect } from "react";
import PropTypes from "prop-types";
import SaveButton from "./SaveButton";
import { Grid, Ref, Card, Header } from "semantic-ui-react";
import { connect } from "react-redux";
import { getLocalizedValue } from "@js/oarepo_ui/util";
import { getIn, useFormikContext } from "formik";
import { useSanitizeInput } from "@js/oarepo_ui/forms";
import FormFieldsContainer from "./FormFieldsContainer";

export const FormTitle = () => {
  const { values } = useFormikContext();
  const { sanitizeInput } = useSanitizeInput();

  const recordTitle =
    getIn(values, "metadata.title", "") ||
    getLocalizedValue(getIn(values, "title", "")) ||
    "";

  const sanitizedTitle = sanitizeInput(recordTitle);

  return (
    sanitizedTitle && (
      <Header as="h1">
        {/* cannot set dangerously html to SUI header directly, I think it is some internal
        implementation quirk (it says you cannot have both children and dangerouslySethtml even though
        there is no children given to the component) */}
        <span dangerouslySetInnerHTML={{ __html: sanitizedTitle }} />
      </Header>
    )
  );
};

const BaseFormLayoutComponent = ({ record, errors = {} }) => {
  const sidebarRef = React.useRef(null);
  const formFeedbackRef = React.useRef(null);
  // on chrome there is an annoying issue where after deletion you are redirected, and then
  // if you click back on browser <-, it serves you the deleted page, which does not exist from the cache.
  // on firefox it does not happen.
  useEffect(() => {
    const handleUnload = () => {};

    const handleBeforeUnload = () => {};

    window.addEventListener("unload", handleUnload);
    window.addEventListener("beforeunload", handleBeforeUnload);

    return () => {
      window.removeEventListener("unload", handleUnload);
      window.removeEventListener("beforeunload", handleBeforeUnload);
    };
  }, []);

  return (
    <Grid>
      <Ref innerRef={formFeedbackRef}>
        <Grid.Column id="main-content" mobile={16} tablet={16} computer={11}>
          <FormTitle />
          <FormFieldsContainer />
        </Grid.Column>
      </Ref>
      <Ref innerRef={sidebarRef}>
        <Grid.Column id="control-panel" mobile={16} tablet={16} computer={5}>
          <Card fluid>
            <Card.Content>
              <Grid relaxed>
                <Grid.Column computer={16} mobile={16}>
                  <SaveButton fluid positive />
                </Grid.Column>
              </Grid>
            </Card.Content>
          </Card>
        </Grid.Column>
      </Ref>
    </Grid>
  );
};

const mapStateToProps = (state) => {
  return {
    record: state.deposit.record,
    errors: state.deposit.errors,
  };
};

export const BaseFormLayout = connect(
  mapStateToProps,
  null
)(BaseFormLayoutComponent);

BaseFormLayoutComponent.propTypes = {
  record: PropTypes.object.isRequired,
  // eslint-disable-next-line react/require-default-props
  errors: PropTypes.object,
  // eslint-disable-next-line react/require-default-props
  formikProps: PropTypes.object,
};

export default BaseFormLayout;
