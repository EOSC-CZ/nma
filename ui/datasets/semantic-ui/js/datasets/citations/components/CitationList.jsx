import React from "react";
import PropTypes from "prop-types";

import CitationListItem from "./CitationListItem";

import { List } from "semantic-ui-react";

const CitationList = ({ record }) => {
  console.log(JSON.stringify(record));

  return (
    <List size="small">
      <CitationListItem recordLink={record.links.self} style="apa" label="APA" />
      <CitationListItem recordLink={record.links.self} style="harvard-cite-them-right" label="Harvard" />
      <CitationListItem recordLink={record.links.self} style="modern-language-association" label="MLA" />
      <CitationListItem recordLink={record.links.self} style="vancouver" label="Vancouver" />
      <CitationListItem recordLink={record.links.self} style="chicago-fullnote-bibliography" label="Chicago" />
      <CitationListItem recordLink={record.links.self} style="ieee" label="IEEE" />
    </List>
  );
};

CitationList.propTypes = {
  record: PropTypes.object.isRequired,
};

export default CitationList;
