import PropTypes from "prop-types";
import { withState } from "react-searchkit";
import { Card } from "semantic-ui-react";
import _get from "lodash/get";
import _truncate from "lodash/truncate";

// TODO: Update this according to the full List item template?
export const ResultsGridItem = ({ result }) => {
  const descriptionStripped = _get(
    result,
    "ui.description_stripped",
    "No description"
  );
  return (
    <Card fluid href={`/docs/${result.links.self}`}>
      <Card.Content>
        <Card.Header>{result.metadata.title}</Card.Header>
        <Card.Description>
          {_truncate(descriptionStripped, { length: 200 })}
        </Card.Description>
      </Card.Content>
    </Card>
  );
};

ResultsGridItem.propTypes = {
  result: PropTypes.object.isRequired,
};

const ResultsGridItemWithState = withState(
  ({ currentQueryState, result, appName }) => (
    <ResultsGridItem
      currentQueryState={currentQueryState}
      result={result}
      appName={appName}
    />
  )
);

export default ResultsGridItemWithState;

ResultsGridItemWithState.propTypes = {
  currentQueryState: PropTypes.object,
  result: PropTypes.object.isRequired,
};

ResultsGridItemWithState.defaultProps = {
  currentQueryState: null,
};
