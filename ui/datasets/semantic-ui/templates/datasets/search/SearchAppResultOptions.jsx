import React, { useContext } from "react";
import Overridable from "react-overridable";
import { PropTypes } from "prop-types";
import { LayoutSwitcher } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";
import { SearchAppSort } from '@js/oarepo_ui/search';
import { i18next } from "@translations/oarepo_ui/i18next";

const SearchAppResultOptions = ({ sortOptions, layoutOptions }) => {
  const { buildUID } = useContext(SearchConfigurationContext);
  const multipleLayouts =
    Object.values(layoutOptions).filter((i) => i).length > 1;
  return (
    <>
      {sortOptions && (
        <div className="search-sort">
          <span>{i18next.t('Sort')}:</span>
          <Overridable id={buildUID("SearchApp.sort")} options={sortOptions}>
            <SearchAppSort />
          </Overridable>
        </div>
      )}
      {multipleLayouts && <LayoutSwitcher />}
    </>
  );
};

SearchAppResultOptions.propTypes = {
  sortOptions: PropTypes.arrayOf(
    PropTypes.shape({
      sortBy: PropTypes.string,
      text: PropTypes.string,
    })
  ),
  paginationOptions: PropTypes.shape({
    defaultValue: PropTypes.number,
    resultsPerPage: PropTypes.array,
  }),
  layoutOptions: PropTypes.object,
};

export default SearchAppResultOptions;
