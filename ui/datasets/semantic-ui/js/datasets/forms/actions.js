import { _saveDraft } from "@js/oarepo_ui/forms/state/deposit/actions";
import {
  DRAFT_HAS_VALIDATION_ERRORS,
  DRAFT_SAVE_FAILED,
  DRAFT_SAVE_STARTED,
  DRAFT_SAVE_SUCCEEDED,
} from "@js/invenio_rdm_records/src/deposit/state/types";

export const save = (
  draft,
  { successMessage, errorMessage, ignoreValidationErrors = false } = {}
) => {
  return async (dispatch, getState, config) => {
    dispatch({ type: DRAFT_SAVE_STARTED });

    const response = await _saveDraft(draft, config.service.drafts, {
      depositState: getState().deposit,
      dispatchFn: dispatch,
      failType: DRAFT_SAVE_FAILED,
      partialValidationActionType: DRAFT_HAS_VALIDATION_ERRORS,
      showOnlyValidationErrorsWithSeverityError: false,
      ignoreValidationErrors,
      successMessage,
      errorMessage,
    });

    const { actionState } = getState().deposit;
    if (actionState === DRAFT_SAVE_SUCCEEDED) {
      window.location.replace(response.data.links.self_html);
    }

    return response;
  };
};
