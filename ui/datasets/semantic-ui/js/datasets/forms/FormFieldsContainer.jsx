import * as React from "react";
import {
  FormikStateLogger,
  TextField,
  CreatibutorsField,
  EDTFSingleDatePicker,
  useFormConfig,
} from "@js/oarepo_ui/forms";
import { connect } from "react-redux";
import PropTypes from "prop-types";

const FormFieldsContainerComponent = ({ record }) => {
  return (
    <React.Fragment>
      <TextField fieldPath="metadata.title" />
      <EDTFSingleDatePicker fieldPath="metadata.publication_date" />
      <CreatibutorsField
        fieldPath="metadata.creators"
        schema="creators"
        autocompleteNames="search"
      />
      {process.env.NODE_ENV === "development" && <FormikStateLogger />}
    </React.Fragment>
  );
};

FormFieldsContainerComponent.propTypes = {
  record: PropTypes.object.isRequired,
};

const mapStateToProps = (state) => {
  return {
    record: state.deposit.record,
  };
};

export default connect(mapStateToProps)(FormFieldsContainerComponent);
