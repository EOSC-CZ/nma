import React, { useEffect, useRef } from "react";
import PropTypes from "prop-types";

import { i18next } from "@translations/i18next";

import { initCopyButtons, deinitializeCopyButtons } from "@datasets_detail";

const ClipboardCopyButton = ({ copyText }) => {
  const copyBtnRef = useRef(null);

  useEffect(() => {
    const copyBtn = copyBtnRef.current;
    if (copyBtn) {
      initCopyButtons(copyBtnRef.current);
    }
    return () => {
      deinitializeCopyButtons(copyBtn);
    }
  }, [copyText]);

  return (
    <i
      ref={copyBtnRef}
      title={`${i18next.t("Click to copy")}: ${copyText}`}
      role="button"
      className="copy outline link teal icon copy-button rel-ml-1"
      data-clipboard-text={copyText}
    />
  );
};

ClipboardCopyButton.propTypes = {
  copyText: PropTypes.string.isRequired,
};

export default ClipboardCopyButton;
