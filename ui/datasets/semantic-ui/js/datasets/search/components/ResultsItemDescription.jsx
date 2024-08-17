import React, { useLayoutEffect, useRef, useState } from 'react'

import { i18next } from "@translations/i18next";
import { Icon, Item } from "semantic-ui-react";
import sanitizeHtml from "sanitize-html";

export const ResultsItemDescription = ({ html, maxLineHeight, selfHtml }) => {
  const contentRef = useRef();
  const [lineHeight, setLineHeight] = useState(0);

  useLayoutEffect(() => {
    if (contentRef.current) {
      const computedStyle = window.getComputedStyle(contentRef.current);
      setLineHeight(Number(computedStyle['line-height'].replace('px', '')));
    }
  }, [maxLineHeight]);

  const contentStyle = {
    display: '-webkit-box',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    WebkitBoxOrient: 'vertical',
    WebkitLineClamp: maxLineHeight,
  };

  return (
    <Item.Description 
      className="listing-item-description" 
      style={{ height: `${maxLineHeight * lineHeight}px` }}
    >
      <span
        dangerouslySetInnerHTML={{
          __html: sanitizeHtml(html)
        }}
        ref={contentRef}
        style={contentStyle}
      />
      <a href={selfHtml} className="read-more-link">
        {i18next.t("read more")}
        <Icon name="chevron right" link className="read-more-chevron" />
      </a>
    </Item.Description>
  );
}
