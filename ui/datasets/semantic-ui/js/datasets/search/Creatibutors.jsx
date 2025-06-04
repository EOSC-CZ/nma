import React, { useState } from "react";
import PropTypes from "prop-types";
import { Button, Icon, List, ListItem, Accordion, AccordionTitle } from "semantic-ui-react";
import creatibutor, { Creatibutor } from "./Creatibutor";


const CreatibutorsList = ({ creatibutors, showAll, numDisplayed }) => {
    const displayedCreatibutors = showAll
    ? creatibutors
    : creatibutors?.slice(0, numDisplayed);

    return (
        <List horizontal verticalAlign="middle" className="results-list-item creatibutors">
        {displayedCreatibutors.map((creatibutor, index) => (
          <ListItem key={`person-${index}`}>
            <Creatibutor creatibutor={creatibutor} />
            {index < displayedCreatibutors.length - 1 ? "; " : null}
          </ListItem>
        ))};
          {creatibutors.length > numDisplayed && (
            <>
              {!showAll && <ListItem> et al.</ListItem>}
              <ListItem key="icon-expand-accordion">
                <Icon size="small" name="right chevron" color="green" />
              </ListItem>
            </>
          )}
      </List>
    );
}

export const Creatibutors = ({ creatibutors }) => {
  const [showAllPersons, setShowAllPersons] = useState(false);
  const [showAllOrgs, setShowAllOrgs] = useState(false);

  const togglePersons = () => {
    setShowAllPersons(!showAllPersons);
  };

  const toggleOrgs = () => {
    setShowAllOrgs(!showAllOrgs);
  };

  const personalCreatibutors = creatibutors?.filter((c) => !!c.person) || [];
  const orgCreatibutors = creatibutors?.filter((c) => !!c.organization) || [];
  // there can be a significant number of contributors, and it can get unreadable
  const numDisplayed = 4

  return (
    <>
      <Accordion>
        <AccordionTitle
          active={showAllPersons}
          index={0}
          onClick={togglePersons}
        >
          <CreatibutorsList creatibutors={personalCreatibutors} showAll={showAllPersons} numDisplayed={numDisplayed} />
        </AccordionTitle>
      </Accordion>
      <Accordion style={{ marginTop: "-1rem" }}>
        <AccordionTitle
          active={showAllOrgs}
          index={0}
          onClick={toggleOrgs}
        >
          <CreatibutorsList creatibutors={orgCreatibutors} showAll={showAllOrgs} numDisplayed={numDisplayed} />
        </AccordionTitle>
      </Accordion>
    </>
  );
};

Creatibutors.propTypes = { creatibutors: PropTypes.array.isRequired };

export default Creatibutors;
