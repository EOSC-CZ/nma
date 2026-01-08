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
import { ResourceTypeField } from "@js/invenio_rdm_records";

const FormFieldsContainerComponent = ({ record }) => {
  const {
    config: { vocabularies },
  } = useFormConfig();
  return (
    <React.Fragment>
      <TextField fieldPath="metadata.title" />
      <ResourceTypeField
        options={vocabularies.resource_type}
        fieldPath="metadata.resource_type"
        required
        upward={false}
      />
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
