import React, { useState } from "react";
import PropTypes from "prop-types";

import { i18next } from "@translations/i18next";
import { Button } from "semantic-ui-react";

const ClipboardCopyButton = ({ copyText }) => {
  const [isCopied, setIsCopied] = useState(false);

  // This is the function we wrote earlier
  async function copyTextToClipboard(text) {
    if ("clipboard" in navigator) {
      return await navigator.clipboard.writeText(text);
    } else {
      return document.execCommand("copy", true, text);
    }
  }

  // onClick handler function for the copy button
  const handleCopyClick = () => {
    // Asynchronously call copyTextToClipboard
    copyTextToClipboard(copyText)
      .then(() => {
        // If successful, update the isCopied state value
        setIsCopied(true);
        setTimeout(() => {
          setIsCopied(false);
        }, 500);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <Button title={i18next.t(`Press to copy: ${copyText}`)} onClick={handleCopyClick} loading={isCopied} icon="copy" />
  );
};

ClipboardCopyButton.propTypes = {
  copyText: PropTypes.string.isRequired,
};

export default ClipboardCopyButton;
