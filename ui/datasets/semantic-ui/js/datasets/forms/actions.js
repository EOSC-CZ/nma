import { save as invenioSave } from "@js/invenio_rdm_records/src/deposit/state/actions/deposit";
import { DRAFT_SAVE_SUCCEEDED } from "@js/invenio_rdm_records/src/deposit/state/types";

export const save = (draft) => {
  return async (dispatch, getState) => {
    await dispatch(invenioSave(draft));
    if (getState().deposit.actionState === DRAFT_SAVE_SUCCEEDED) {
      const url = getState().deposit.record?.links?.self_html;
      if (url) window.location.replace(url);
    }
  };
};
