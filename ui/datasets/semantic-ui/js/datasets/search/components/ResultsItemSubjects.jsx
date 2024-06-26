import React from "react";
import PropTypes from "prop-types";
import _groupBy from "lodash/groupBy";
import _has from "lodash/has";
import _partition from "lodash/partition";
import _concat from "lodash/concat";
import { Label, List } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { SearchFacetLink } from "./SearchFacetLink";

const SubjectElement = ({ searchUrl, subject }) => (
  <SearchFacetLink
    searchUrl={searchUrl}
    searchFacet={"metadata_subjects_subject"}
    value={subject.subject}
    title={i18next.t("Find more records with this subject")}
    className="subject-link"
  />
);

SubjectElement.propTypes = {
  subject: PropTypes.object.isRequired,
  searchUrl: PropTypes.string,
};

export function ResultsItemSubjects({
  subjects,
  searchUrl,
  maxCount = 6,
  ...rest
}) {
  const [withLang, withoutLang] = _partition(subjects, (s) => _has(s, "lang"));
  const langGroups = _groupBy(withLang, "lang");
  langGroups["undefined"] = withoutLang;
  console.log(langGroups);
  return Object.entries(langGroups).map(([lang, values]) => (
    <div key={lang}>
      <List horizontal className="subjects">
        {values.slice(0, maxCount).map((sub) => (
          <List.Item
            key={`${sub.lang}-${sub.subject}-${sub.valueURI}`}
          >
            <List.Content verticalAlign="middle">
              <Label size="small" color="teal" basic className="keyword-subjects">
                {(lang && lang !== 'undefined') ? lang.toUpperCase() : ''}&nbsp;<SubjectElement searchUrl={searchUrl} subject={sub} />
              </Label>
            </List.Content>
          </List.Item>
        ))}
        {values.length > maxCount && <List.Item>...</List.Item>}
      </List>
    </div>
  ));
}

ResultsItemSubjects.propTypes = {
  searchUrl: PropTypes.string,
  subjects: PropTypes.array.isRequired,
  maxCount: PropTypes.number,
};

ResultsItemSubjects.defaultProps = {
  maxCount: 6,
};
