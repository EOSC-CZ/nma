from flask_resources import (
    ResponseHandler,
)
from flask import request
from invenio_records_resources.resources.records.headers import etag_headers
from .csl import CSLJSONSerializer, StringCitationSerializer

def csl_url_args_retriever():
    """Returns the style and locale passed as URL args for CSL export."""
    style = request.args.get("style")
    locale = request.args.get("locale")
    return style, locale


#
# Response handlers
#
def _bibliography_headers(obj_or_list, code, many=False):
    """Override content type for 'text/x-bibliography'."""
    _etag_headers = etag_headers(obj_or_list, code, many=False)
    _etag_headers["content-type"] = "text/plain"
    return _etag_headers

citations_response_handlers = {
    "application/vnd.citationstyles.csl+json": ResponseHandler(
        CSLJSONSerializer(), headers=etag_headers
    ),
    "text/x-bibliography": ResponseHandler(
        StringCitationSerializer(url_args_retriever=csl_url_args_retriever),
        headers=_bibliography_headers,
    )
}