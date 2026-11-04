import React, { useState, useEffect } from "react";
import { i18next } from "@translations/oarepo_ui/i18next";
import { ClipboardCopyButton } from "@js/oarepo_ui/components/ClipboardCopyButton";

export const CopyButton = ({ url }) => {
  const [exportData, setExportData] = useState("");

  useEffect(() => {
    let isMounted = true;

    const fetchExportData = async () => {
      if (!url) return;
      try {
        const response = await fetch(url);
        const text = await response.text();

        if (isMounted) {
          setExportData(text);
        }
      } catch (error) {
        console.error(`Failed to fetch export data <${error}>!`);
      }
    };

    fetchExportData();

    return () => {
      isMounted = false;
    };
  }, [url]);

  return (
    <div title={i18next.t("Copy to clipboard")}>
      <ClipboardCopyButton copyText={exportData || url} />
    </div>
  );
};
