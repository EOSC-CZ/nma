import { i18next } from "@translations/invenio_app_rdm/i18next";
import _get from "lodash/get";
import React, { Component } from "react";
import { SearchItemCreators } from "@js/invenio_app_rdm/utils";
import PropTypes from "prop-types";
import { Item, Label, Icon } from "semantic-ui-react";

class ResultsListItem extends Component {
  render() {
    const { result } = this.props;

    const viewLink = _get(result, "links.self_html");
    const createdDate = _get(
      result,
      "ui.created_date_l10n_long",
      i18next.t("No creation date found.")
    );

    const creators = _get(result, "ui.creators.creators", []);

    const descriptionStripped = _get(result, "ui.description_stripped");

    const publicationDate = _get(
      result,
      "ui.publication_date_l10n_long",
      i18next.t("No publication date found.")
    );
    const resourceType = _get(
      result,
      "ui.resource_type.title_l10n",
      i18next.t("No resource type")
    );
    const subjects = _get(result, "ui.subjects", []);
    const title = _get(result, "metadata.title", i18next.t("No title"));

    const publishingInformation = _get(
      result,
      "ui.publishing_information.journal",
      ""
    );

    return (
      <Item
        key={result.id}
        data-testid="result-item"
        className="search-result-item"
      >
        <Item.Content>
          <Item.Extra className="labels-actions">
            <Label horizontal size="small" className="primary theme-primary">
              {publicationDate}
            </Label>
            <Label horizontal size="small" className="neutral">
              {resourceType}
            </Label>
            <Label horizontal size="small" className="basic green">
              {result.metadata.persistent_url}
            </Label>
          </Item.Extra>
          <Item.Header as="h2" className="theme-primary-text">
            <a href={viewLink}>{title}</a>
          </Item.Header>
          <Item className="creatibutors">
            <SearchItemCreators creators={creators} othersLink={viewLink} />
          </Item>
          {descriptionStripped && (
            <Item.Description className="truncate-lines-2">
              {descriptionStripped}
            </Item.Description>
          )}

          <Item.Extra>
            {subjects.map((subject, idx) => (
              <Label key={`${subject.title_l10n}-${idx}`} size="tiny">
                {subject.title_l10n}
              </Label>
            ))}

            <p>
              <small>
                {createdDate && (
                  <>
                    {i18next.t("Uploaded on {{uploadDate}}", {
                      uploadDate: createdDate,
                    })}
                  </>
                )}
                {createdDate && publishingInformation && " | "}

                {publishingInformation && (
                  <>
                    {i18next.t("Published in: {{- publishInfo }}", {
                      publishInfo: publishingInformation,
                    })}
                  </>
                )}
              </small>
            </p>
          </Item.Extra>
        </Item.Content>
      </Item>
    );
  }
}

ResultsListItem.propTypes = {
  result: PropTypes.object.isRequired,
};

export default ResultsListItem;
