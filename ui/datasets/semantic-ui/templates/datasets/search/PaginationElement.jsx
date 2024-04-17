import React from "react";
import PropTypes from "prop-types";
import { Pagination, Icon } from "semantic-ui-react";

const PaginationElement = ({
  id,
  currentPage,
  currentSize,
  totalResults,
  onPageChange,
  options,
  maxTotalResults,
  ...props
}) => {
  const boundaryRangeCount = options.boundaryRangeCount;
  const siblingRangeCount = options.siblingRangeCount;
  const showEllipsis = options.showEllipsis;
  const showFirst = options.showFirst;
  const showLast = options.showLast;
  const showPrev = options.showPrev;
  const showNext = options.showNext;
  const size = options.size;

  const maxTotalPages = Math.floor(maxTotalResults / currentSize);
  const pages = Math.ceil(totalResults / currentSize);
  const totalDisplayedPages = Math.min(pages, maxTotalPages);

  if (currentPage > pages) onPageChange(pages);

  return (
    <Pagination
      text
      color="teal"
      activePage={currentPage}
      totalPages={totalDisplayedPages}
      onPageChange={(_, { activePage }) => onPageChange(activePage)}
      boundaryRange={boundaryRangeCount}
      siblingRange={siblingRangeCount}
      ellipsisItem={showEllipsis ? undefined : null}
      firstItem={showFirst ? undefined : null}
      lastItem={showLast ? undefined : null}
      prevItem={showPrev ? undefined : null}
      nextItem={showNext ? undefined : null}
      size={size}
      {...props}
    />
  );
};

PaginationElement.propTypes = {
  currentPage: PropTypes.number.isRequired,
  currentSize: PropTypes.number.isRequired,
  totalResults: PropTypes.number.isRequired,
  onPageChange: PropTypes.func.isRequired,
  options: PropTypes.object,
  maxTotalResults: PropTypes.number,
};

PaginationElement.defaultProps = {
  options: {},
  maxTotalResults: 10000,
};

export default PaginationElement;
