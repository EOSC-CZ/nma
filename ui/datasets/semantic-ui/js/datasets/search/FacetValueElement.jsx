import * as React from 'react';
import { ContribBucketAggregationValuesElement } from "@js/invenio_search_ui/components";
import { i18next } from "@translations/i18next";

export const FacetValueElement = (props) => {
    const {children, bucket, ...rest} = props;

    const bucketLabelWithUnfilled = bucket.label !== ""? bucket : ({ ...bucket, label: i18next.t("Unfilled") });

    return <ContribBucketAggregationValuesElement bucket={bucketLabelWithUnfilled} {...rest}>
        {children}
    </ContribBucketAggregationValuesElement>
};