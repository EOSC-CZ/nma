import React, { useState } from "react";
import PropTypes from "prop-types";
import { Icon, List, ListItem, Accordion, AccordionTitle } from "semantic-ui-react";
import { Creatibutor } from "./Creatibutor";

const CreatibutorsList = ({ creatibutors, showAll, numDisplayed }) => {
  const displayedCreatibutors = showAll ? creatibutors : creatibutors?.slice(0, numDisplayed);

  return (
    <List horizontal verticalAlign="middle" className="results-list-item creatibutors">
      {displayedCreatibutors.map((creatibutor, index) => (
        <ListItem key={`person-${index}`}>
          <Creatibutor creatibutor={creatibutor} />
          {index < displayedCreatibutors.length - 1 ? "; " : null}
        </ListItem>
      ))}
      {creatibutors.length > numDisplayed && (
        <>
          {!showAll && <ListItem> et al.</ListItem>}
          <ListItem key="icon-expand-accordion">
            <Icon size="small" role="button" name="right chevron" color="primary" fitted aria-label={showAll ? i18next.t("Show less") : i18next.t("Show more")} />
          </ListItem>
        </>
      )}
    </List>
  );
};

CreatibutorsList.propTypes = {
  creatibutors: PropTypes.array.isRequired,
  showAll: PropTypes.bool.isRequired,
  numDisplayed: PropTypes.number.isRequired,
};

export const Creatibutors = ({ creatibutors }) => {
  const [showAllPersons, setShowAllPersons] = useState(false);
  const [showAllOrgs, setShowAllOrgs] = useState(false);

  const togglePersons = () => {
    setShowAllPersons(!showAllPersons);
  };

  const toggleOrgs = () => {
    setShowAllOrgs(!showAllOrgs);
  };

  const personalCreatibutors = creatibutors?.filter((c) => c.person_or_org?.type !== "organizational") || [];
  const orgCreatibutors = creatibutors?.filter((c) => c.person_or_org?.type === "organizational") || [];
  const numDisplayed = 4;

  return (
    <>
      {personalCreatibutors.length > 0 && (
        <Accordion>
          <AccordionTitle active={showAllPersons} index={0} onClick={togglePersons}>
            <CreatibutorsList
              creatibutors={personalCreatibutors}
              showAll={showAllPersons}
              numDisplayed={numDisplayed}
            />
          </AccordionTitle>
        </Accordion>
      )}
      {orgCreatibutors.length > 0 && (
        <Accordion style={personalCreatibutors.length > 0 ? { marginTop: "-1rem" } : {}}>
          <AccordionTitle active={showAllOrgs} index={0} onClick={toggleOrgs}>
            <CreatibutorsList
              creatibutors={orgCreatibutors}
              showAll={showAllOrgs}
              numDisplayed={numDisplayed}
            />
          </AccordionTitle>
        </Accordion>
      )}
    </>
  );
};

Creatibutors.propTypes = { creatibutors: PropTypes.array.isRequired };

export default Creatibutors;
