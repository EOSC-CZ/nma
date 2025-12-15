import { RecordManagement } from "./RecordManagement";
import ReactDOM from "react-dom";
import React from "react";

const recordManagementAppDiv = document.getElementById("recordManagementMenu");
const recordManagementMobile = document.getElementById(
  "recordManagementMobileMenu"
);
if (recordManagementAppDiv) {
  renderRecordManagement(recordManagementAppDiv);
  recordManagementMobile && renderRecordManagement(recordManagementMobile);
}

function renderRecordManagement(element) {
  const record = JSON.parse(recordManagementAppDiv.dataset.record);
  ReactDOM.render(
    <RecordManagement
      record={record}
      permissions={JSON.parse(recordManagementAppDiv.dataset.permissions)}
      isPreviewSubmissionRequest={JSON.parse(
        recordManagementAppDiv.dataset.isPreviewSubmissionRequest
      )}
      currentUserId={recordManagementAppDiv.dataset.currentUserId}
      recordOwnerID={record.parent.access.owned_by.user}
      groupsEnabled={JSON.parse(recordManagementAppDiv.dataset.groupsEnabled)}
      recordDeletion={JSON.parse(recordManagementAppDiv.dataset.recordDeletion)}
      recordDeletionOptions={JSON.parse(
        recordManagementAppDiv.dataset.recordDeletionOptions
      )}
    />,
    element
  );
}

$("#manage-record-btn").popup({
  popup: $("#recordManagementMobileMenu"),
  on: "click",
  position: "bottom right",
  onVisible: function ($module) {
    $($module).attr("aria-expanded", true);
  },
  onHidden: function ($module) {
    $($module).attr("aria-expanded", false);
  },
});
