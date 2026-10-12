/*
 * SPDX-FileCopyrightText: 2026 CESNET z.s.p.o.
 * SPDX-License-Identifier: MIT
 */

import ReactDOM from "react-dom";
import React from "react";
import { DatasetsRecordManagement } from "./RecordManagement";

// Mounts the datasets manage-menu (Edit via ``record.links.edit_html`` +
// Share, no "New version") into the record-detail page's own mount point
// (#dataset-record-management). Stock ``landing-page.js`` is not used for the
// manage menu here because the datasets record_detail's ``manage_menu.html``
// intentionally omits the stock #recordManagement id.
const container = document.getElementById("dataset-record-management");
if (container) {
  const record = JSON.parse(container.dataset.record);

  ReactDOM.render(
    <DatasetsRecordManagement
      record={record}
      permissions={JSON.parse(container.dataset.permissions)}
      groupsEnabled={JSON.parse(container.dataset.groupsEnabled)}
    />,
    container
  );
}
