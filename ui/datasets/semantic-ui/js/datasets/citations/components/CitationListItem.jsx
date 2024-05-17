import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

import axios from "axios";
import { withCancel } from "react-invenio-forms";
import { i18next } from "@translations/i18next";

import { List, Placeholder, Message } from "semantic-ui-react";

import ClipboardCopyButton from "./ClipboardCopyButton";

const CitationListItem = ({ recordLink, style, label = style }) => {
  const [loading, setLoading] = useState(false);
  const [citation, setCitation] = useState("");
  const [error, setError] = useState("");

  let cancellableFetchCitation = null;

  useEffect(() => {
    getCitation(recordLink, style);
    return () => cancellableFetchCitation?.cancel();
  }, []);

  const PlaceholderLoader = () => {
    return (
      <Placeholder role="presentation">
        <Placeholder.Paragraph>
          <Placeholder.Line />
          <Placeholder.Line />
          <Placeholder.Line />
        </Placeholder.Paragraph>
      </Placeholder>
    );
  };

  const ErrorMessage = ({ message }) => {
    return <Message negative role="status" aria-label={i18next.t(`Error generating ${label} citation`)}>{message}</Message>;
  };

  const fetchCitation = async (recordLink, style) => {
    const locale = i18next.language === "cs" ? "cs-CZ" : i18next.language === "en" ? "en-US" : i18next.language;
    const url = `${recordLink}?locale=${locale}&style=${style}`;
    return await axios(url, {
      headers: {
        Accept: "text/x-bibliography",
      },
    });
  };

  const getCitation = async (record, style) => {
    setLoading(true);
    setCitation("");
    setError("");

    cancellableFetchCitation = withCancel(
      fetchCitation(record, style)
    );

    try {
      const response = await cancellableFetchCitation.promise;
      setLoading(false);
      setCitation(response.data);
    } catch (error) {
      if (error !== "UNMOUNTED") {
        setLoading(false);
        setCitation("");
        setError(i18next.t("An error occurred while generating the citation."));
      }
    }
  };

  return (
    <List.Item >
      {!error &&
        <List.Content floated="right">
          <ClipboardCopyButton copyText={citation} />
        </List.Content>
      }
      <List.Content as="article">
        <List.Header as="h3">{label}</List.Header>
        <List.Description>
          {(loading && <PlaceholderLoader />) || citation}
          {error && <ErrorMessage message={error} />}
        </List.Description>
      </List.Content>
    </List.Item>
  );
};

CitationListItem.propTypes = {
  recordLink: PropTypes.string.isRequired,
  style: PropTypes.string.isRequired,
  label: PropTypes.string,
};

export default CitationListItem;
