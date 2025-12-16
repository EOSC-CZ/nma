// This file is part of InvenioRDM
// Copyright (C) 2020-2025 CERN.
// Copyright (C) 2020-2021 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.
import { i18next } from "@translations/invenio_app_rdm/i18next";

import React, { Component } from "react";
import { Button, Grid, Icon, Message } from "semantic-ui-react";
import { ShareButton } from "@js/invenio_app_rdm/landing_page/ShareOptions/ShareButton";
import PropTypes from "prop-types";

export class RecordManagement extends Component {
  render() {
    const { record, permissions, groupsEnabled } = this.props;
    return (
      <Grid columns={1} className="record-management">
        {permissions.can_update && (
          <Grid.Column className="pb-10">
            <Button
              fluid
              size="medium"
              onClick={() => (window.location = record.links?.edit_html)}
              icon
              labelPosition="left"
            >
              <Icon name="edit" />
              {i18next.t("Edit")}
            </Button>
          </Grid.Column>
        )}
        {permissions.can_manage && (
          <Grid.Column className={permissions.can_update ? "pt-0" : "pt-20"}>
            <ShareButton
              record={record}
              permissions={permissions}
              groupsEnabled={groupsEnabled}
            />
          </Grid.Column>
        )}
      </Grid>
    );
  }
}

RecordManagement.propTypes = {
  record: PropTypes.object.isRequired,
  permissions: PropTypes.object.isRequired,
  groupsEnabled: PropTypes.bool.isRequired,
};
