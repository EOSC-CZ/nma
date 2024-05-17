import React from "react";
import ReactDOM from "react-dom";

import { RecordCitationModal } from "./components";

const recordCitationsAppDiv = document.getElementById("record-citations");
ReactDOM.render(
  <RecordCitationModal
    record={JSON.parse(recordCitationsAppDiv.dataset.record)}
  />,
  recordCitationsAppDiv
);
