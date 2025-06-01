import React, { useState } from "react";
import PropTypes from "prop-types";
import { Button, Icon } from "semantic-ui-react";
import { Creatibutor } from "./Creatibutor";

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
  const displayedPersons = showAllPersons
    ? personalCreatibutors
    : personalCreatibutors?.slice(0, numDisplayed);

  const displayedOrgs = showAllOrgs
    ? orgCreatibutors
    : orgCreatibutors?.slice(0, numDisplayed);

  return (
    <div className="results-list-item creatibutors">
      <div>
        {displayedPersons?.map((creatibutor, index) => (
          <React.Fragment key={`person-${index}`}>
            <Creatibutor creatibutor={creatibutor} />
            {index < displayedPersons.length - 1 ? "; " : null}
          </React.Fragment>
        ))}
        {personalCreatibutors.length > numDisplayed && (
          <>
            {
              showAllPersons ? null : <span> et al. </span>
            }
            <Button
              compact
              size="tiny"
              onClick={togglePersons}
              className="transparent mr-3"
            >
              {showAllPersons ? (
                <Icon name="left chevron" color="green" />
              ) : (
                <Icon name="right chevron" color="green" />
              )}
            </Button>
          </>
        )}
      </div>

      <div className="mt-2">
        {displayedOrgs?.map((creatibutor, index) => (
          <React.Fragment key={`org-${index}`}>
            <Creatibutor creatibutor={creatibutor} />
            {index < displayedOrgs.length - 1 ? "; " : null}
          </React.Fragment>
        ))}
        {orgCreatibutors.length > 10 && (
          <Button
            compact
            size="tiny"
            onClick={toggleOrgs}
            className="transparent mr-3"
          >
            {showAllOrgs ? (
              <Icon name="left chevron" color="green" />
            ) : (
              <Icon name="right chevron" color="green" />
            )}
          </Button>
        )}
      </div>
    </div >
  );
};

Creatibutors.propTypes = { creatibutors: PropTypes.array.isRequired };

export default Creatibutors;
