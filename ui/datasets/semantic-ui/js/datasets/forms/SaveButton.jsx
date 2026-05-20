import React from "react";
import { Button } from "semantic-ui-react";
import { useDispatch, useSelector } from "react-redux";
import { useFormikContext } from "formik";
import { i18next } from "@translations/invenio_rdm_records/i18next";
import { DRAFT_SAVE_STARTED } from "@js/invenio_rdm_records/src/deposit/state/types";
import { save } from "./actions";

export const SaveButton = (props) => {
  const dispatch = useDispatch();
  const actionState = useSelector((state) => state.deposit.actionState);
  const { values, isSubmitting, setSubmitting } = useFormikContext();

  const handleSave = async () => {
    setSubmitting(true);
    try {
      await dispatch(save(values));
    } catch {
      // errors land in state.deposit.errors; BaseFormLayout bridges them into Formik
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Button
      name="save"
      disabled={isSubmitting}
      onClick={handleSave}
      icon="save"
      loading={isSubmitting && actionState === DRAFT_SAVE_STARTED}
      labelPosition="left"
      content={i18next.t("Save draft")}
      {...props}
    />
  );
};

export default SaveButton;
