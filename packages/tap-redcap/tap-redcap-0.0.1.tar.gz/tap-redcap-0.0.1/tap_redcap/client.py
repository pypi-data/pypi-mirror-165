"""REST client handling, including redcapStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union, cast

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class RedCapStream(RESTStream):
    """redcap stream class."""

    # TODO: Set the API's base URL here:
    url_base = "https://redcap.chop.edu/api/"

    # OR use a dynamic url_base:
    # @property
    # def url_base(self) -> str:
    #     """Return the API URL root, configurable via tap settings."""
    #     return self.config["api_url"]

    records_jsonpath = "$[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.next_page"  # Or override `get_next_page_token`.

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        # TODO: If pagination is required, return a token which can be used to get the
        #       next page. If this is the final page, return "None" to end the
        #       pagination loop.
        if self.next_page_token_jsonpath:
            all_matches = extract_jsonpath(
                self.next_page_token_jsonpath, response.json()
            )
            first_match = next(iter(all_matches), None)
            next_page_token = first_match
        else:
            next_page_token = response.headers.get("X-Next-Page", None)

        return next_page_token

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    #overrides RESTStream::prepare_request_payload
    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        return {
            "token": self.config["token"],
            "content": self.config["content"],
            "action": self.config["action"],
            "format": self.config["format"],
            "type": self.config["type"],
            "forms": self.forms,
            "events": self.config["events"],
            "rawOrLabel": self.config["rawOrLabel"],
            "rawOrLabelHeaders": self.config["rawOrLabelHeaders"],
            "exportCheckboxLabel": self.config["exportCheckboxLabel"],
            "exportSurveyFields": self.config["exportSurveyFields"],
            "returnFormat": self.config["returnFormat"],
            "exportDataAccessGroups": self.config["exportDataAccessGroups"]
        }
        
    # overrides RESTStream::prepare_request
    def prepare_request(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> requests.PreparedRequest:
        request_data = self.prepare_request_payload(context, next_page_token)

        request = cast( 
            requests.PreparedRequest,
            self.requests_session.prepare_request(
                requests.Request(
                    method="POST",
                    url=self.url_base,
                    data=request_data,
                ),
            ),
        )
        return request

