import React from "react";
import { Card, Grid } from "semantic-ui-react";
import { SaveButton, PublishButton, PreviewButton, ValidateButton, DeleteButton } from "@js/oarepo_ui";


export const FormActionsContainer = ({ record }) => {
  return (
    <Card fluid>
      <Card.Content>
        <Grid>
          <Grid.Column computer={8} mobile={16} className="left-btn-col">
            <SaveButton fluid />
          </Grid.Column>
          <Grid.Column computer={8} mobile={16} className="right-btn-col">
            <PreviewButton fluid />
          </Grid.Column>
          <Grid.Column width={16} className="pt-10">
            <PublishButton />
          </Grid.Column>
          <Grid.Column width={16} className="pt-10">
            <ValidateButton />
          </Grid.Column>
          <Grid.Column width={16} className="pt-10">
          <DeleteButton redirectUrl="/datasets/" />
        </Grid.Column>
        </Grid>
      </Card.Content>
    </Card>
  );
};

export default FormActionsContainer;
