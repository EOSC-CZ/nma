import React, { useEffect, useState, useRef, useCallback } from "react";
import PropTypes from "prop-types";

import { Placeholder, Dropdown, Message } from "semantic-ui-react";
import { withCancel } from "react-invenio-forms";
import { i18next } from "@translations/invenio_app_rdm/i18next";
import axios from "axios";
import _debounce from "lodash/debounce";
import { sanitizeInput } from "@js/oarepo_ui";

import ClipboardCopyButton from "./ClipboardCopyButton";

const CitationField = ({
  styles,
  record,
  defaultStyle,
}) => {
  const [loading, setLoading] = useState(true);
  const [citation, setCitation] = useState("");
  const [error, setError] = useState(null);

  const cancellableFetchCitationRef = useRef(null);

  const recordLink = record.links.self;

  useEffect(() => {
    const cancellableFetchCitation = cancellableFetchCitationRef.current;
    getCitation(recordLink, defaultStyle);

    return () => {
      cancellableFetchCitation?.cancel();
    };
  }, [getCitation, recordLink, defaultStyle]);

  const fetchCitation = async (recordLink, style) => {
    const locale = i18next.language === "cs" ? "cs-CZ" : i18next.language === "en" ? "en-US" : i18next.language;
    const url = `${recordLink}?locale=${locale}&style=${style}`;
    return await axios(url, {
      headers: {
        Accept: "text/x-bibliography",
      },
    });
  };

  const getCitation = useCallback(async (record, style) => {
    setError(null);
    setLoading(true);
    setCitation("");

    const cancellableFetch = withCancel(
      fetchCitation(record, style)
    );
    cancellableFetchCitationRef.current = cancellableFetch;

    try {
      const response = await cancellableFetch.promise;
      setLoading(false);
      setCitation(response.data);
    } catch (error) {
      if (error !== "UNMOUNTED") {
        setLoading(false);
        setCitation("");
        setError(i18next.t("An error occurred while generating the citation."));
      }
    }
  }, []);

  const PlaceholderLoader = () => {
    return (
      <Placeholder fluid role="presentation">
        <Placeholder.Paragraph>
          <Placeholder.Line />
          <Placeholder.Line />
          <Placeholder.Line />
        </Placeholder.Paragraph>
      </Placeholder>
    );
  };

  const ErrorMessage = ({ message }) => {
    return <Message negative role="status" aria-label={i18next.t("Error generating citation.")}>{message}</Message>;
  };

  const escapedCitation = sanitizeInput(citation);
  const urlRegex = /(https?:\/\/[^\s,;]+(?=[^\s,;]*))/g;
  const urlizedCitation = escapedCitation.replace(urlRegex, (url) => {
    let trailingDot = "";
    if (url.endsWith(".")) {
      trailingDot = ".";
      url = url.slice(0, -1);
    }
    return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>${trailingDot}`;
  });

  const citationOptions = styles.map((style) => {
    return {
      key: style.style,
      value: style.style,
      text: style.label,
    };
  });

  const onFieldChange = async (event, data) => {
    setError(null);
    setLoading(true);
    _debounce(
      () => getCitation(recordLink, data.value),
      500
    )();
  }

  return (
    <div>
      {!error ?
        <div id="citation-text" className="wrap-overflowing-text rel-mb-2">
          {loading ? (
            <PlaceholderLoader />
          ) : (
            <div dangerouslySetInnerHTML={{ __html: urlizedCitation }} />
          )}
        </div> :
        <ErrorMessage message={error} />
      }
      <div className="auto-column-grid no-wrap">
        <div className="flex align-items-center">
          <label id="citation-style-label" className="mr-10">
            {i18next.t("Style")}
          </label>
          <Dropdown
            className="citation-dropdown"
            aria-labelledby="citation-style-label"
            defaultValue={defaultStyle}
            options={citationOptions}
            fluid
            selection
            onChange={onFieldChange}
          />
          <ClipboardCopyButton copyText={citation} />
        </div>
      </div>
    </div>
  );
};

CitationField.propTypes = {
  styles: PropTypes.array.isRequired,
  record: PropTypes.object.isRequired,
  defaultStyle: PropTypes.string.isRequired,
};

export default CitationField;
