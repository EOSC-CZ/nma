/*
 * SPDX-FileCopyrightText: 2026 CESNET z.s.p.o.
 * SPDX-License-Identifier: MIT
 */

import { i18next } from "@translations/invenio_app_rdm/i18next";

import React, { Component } from "react";
import { Button, Grid, Icon, Message } from "semantic-ui-react";
import { http } from "react-invenio-forms";
import { ShareButton } from "@js/invenio_app_rdm/landing_page/ShareOptions/ShareButton";
import PropTypes from "prop-types";

// Minimal manage-menu for the datasets record-detail page:
// Edit (resolved via ``record.links.edit_html``, draft created via the upstream
// POST /api/records/:id/draft) and Share. The upstream "New version" button is
// intentionally not rendered.
export class DatasetsRecordManagement extends Component {
  constructor(props) {
    super(props);
    this.state = { loading: false, error: "" };
  }

  handleEditClick = async () => {
    const { record } = this.props;
    const recid = record.id;
    const editHtml = record?.links?.edit_html;

    this.setState({ loading: true });
    try {
      await http.post(
        `/api/records/${recid}/draft`,
        {},
        {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/vnd.inveniordm.v1+json",
          },
        }
      );
      window.location = editHtml;
    } catch (error) {
      this.setState({ loading: false, error: error.response.data.message });
    }
  };

  render() {
    const { record, permissions, groupsEnabled } = this.props;
    const { loading, error } = this.state;
    const editHtml = record?.links?.edit_html;

    return (
      <Grid columns={1} className="record-management">
        {permissions?.can_update && !record?.is_draft && editHtml && (
          <Grid.Column className="pb-5">
            <Button
              fluid
              className="warning"
              size="medium"
              onClick={this.handleEditClick}
              loading={loading}
              icon
              labelPosition="left"
            >
              <Icon name="edit" />
              {i18next.t("Edit")}
            </Button>
          </Grid.Column>
        )}
        {permissions?.can_manage && (
          <Grid.Column className={permissions?.can_update ? "pt-0" : "pt-20"}>
            <ShareButton
              record={record}
              permissions={permissions}
              groupsEnabled={groupsEnabled}
            />
          </Grid.Column>
        )}
        {error && (
          <Grid.Row className="record-management">
            <Grid.Column>
              <Message negative>{error}</Message>
            </Grid.Column>
          </Grid.Row>
        )}
      </Grid>
    );
  }
}

DatasetsRecordManagement.propTypes = {
  record: PropTypes.object.isRequired,
  permissions: PropTypes.object.isRequired,
  groupsEnabled: PropTypes.bool.isRequired,
};
