import React from "react";
import PropTypes from "prop-types";
import { withState } from "react-searchkit";
import { i18next } from "@translations/i18next";
import { Input } from "semantic-ui-react";

export const SearchappSearchbarElement = withState(
  ({
    queryString,
    onInputChange,
    updateQueryState,
    currentQueryState,
    iconColor,
    placeholder: passedPlaceholder,
    actionProps,
  }) => {
    const placeholder = passedPlaceholder || i18next.t("Search");

    const onSearch = () => {
      updateQueryState({ ...currentQueryState, queryString, page: 1 });
    };
    const onBtnSearchClick = () => {
      onSearch();
    };
    const onKeyPress = (event) => {
      if (event.key === "Enter") {
        onSearch();
      }
    };
    return (
      <Input
        action={{
          className: "search",
          color: iconColor,
          content: i18next.t("Search"),
          onClick: onBtnSearchClick,
          "aria-label": i18next.t("Search"),
          ...actionProps,
        }}
        fluid
        placeholder={placeholder}
        aria-label={placeholder}
        onChange={(event, { value }) => {
          onInputChange(value);
        }}
        value={queryString}
        onKeyPress={onKeyPress}
      />
    );
  }
);

SearchappSearchbarElement.propTypes = {
  placeholder: PropTypes.string,
  queryString: PropTypes.string,
  onInputChange: PropTypes.func,
  updateQueryState: PropTypes.func,
  currentQueryState: PropTypes.object,
  iconName: PropTypes.string,
  iconColor: PropTypes.string,
};

SearchappSearchbarElement.defaultProps = {
  placeholder: i18next.t("Search"),
};
