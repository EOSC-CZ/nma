import React, { useContext } from "react";
import { withState } from "react-searchkit";
import { Button } from "semantic-ui-react";
import { i18next } from "@translations/oarepo_ui/i18next";
import PropTypes from "prop-types";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";

// in some cases, there are some permanent facets i.e. in requests open/closed,
// so we have button not remove those initial filters
const ClearFiltersButtonComponent = ({
  updateQueryState,
  currentQueryState,
}) => {
  const { filters } = currentQueryState;
  const searchAppContext = useContext(SearchConfigurationContext);
  const {
    initialQueryState: { filters: initialFilters },
  } = searchAppContext;

  return (
    filters.length > initialFilters?.length && (
      <Button
        name="clear"
        color="orange"
        onClick={() =>
          updateQueryState({
            ...currentQueryState,
            filters: filters.filter((f) =>
              initialFilters.map((f) => f[0]).includes(f[0])
            ),
          })
        }
        icon="delete"
        labelPosition="left"
        content={i18next.t("Clear all filters")}
        type="button"
        size="mini"
      />
    )
  );
};

export const ClearFiltersButton = withState(ClearFiltersButtonComponent);

ClearFiltersButtonComponent.propTypes = {
  updateQueryState: PropTypes.func.isRequired,
  currentQueryState: PropTypes.object.isRequired,
};
