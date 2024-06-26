import React from "react";
import ReactDOM from "react-dom";

import { RecordCitations } from "./components";

const recordCitationsAppDiv = document.getElementById("record-citations");
ReactDOM.render(
  <RecordCitations
    record={JSON.parse(recordCitationsAppDiv.dataset.record)}
  />,
  recordCitationsAppDiv
);
