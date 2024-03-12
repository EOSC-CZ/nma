import React from "react";
import PropTypes from "prop-types";
import _groupBy from "lodash/groupBy";
import { Label, List } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { SearchFacetLink } from "./SearchFacetLink";

const SubjectElement = ({ searchUrl, subject }) => (
  <SearchFacetLink
    searchUrl={searchUrl}
    searchFacet={`metadata_subjects_subject_${subject.subject.lang}_keyword`}
    value={subject.subject.value}
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
  const langGroups = _groupBy(subjects, "subject.lang");

  return Object.entries(langGroups).map(([lang, values]) => (
    <div className="ui separated" key={lang}>
      <Label className="green basic lang-tag">{lang}</Label>
      <List horizontal className="separated subjects">
        {values.slice(0, maxCount).map((sub) => (
          <List.Item
            key={`${sub.subject.lang}-${sub.subject.value}-${sub.valueURI}`}
          >
            <List.Content verticalAlign="middle">
              <SubjectElement searchUrl={searchUrl} subject={sub} />
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
