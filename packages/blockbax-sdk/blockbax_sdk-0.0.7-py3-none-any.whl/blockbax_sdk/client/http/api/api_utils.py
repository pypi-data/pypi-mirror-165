from typing import List, Optional

import requests
import json
import decimal

from blockbax_sdk import errors

import logging

logger = logging.getLogger(__name__)


def parse_response(r: requests.Response) -> Optional[dict]:
    if r.status_code == 404:
        return None
    try:
        return json.loads(r.text)
    except Exception as e:
        raise errors.BlockbaxHTTPError(
            f"Could not parse response: {e}, received status code: {r.status_code}"
        )


# handles HTTP status codes that are not a HTTP error
def response_status_handler(r: requests.Response):
    notify_partial_accepted(r, [207])
    notify_not_found(r, [404])


# Catches different HTTP error cases, either logs errors or raises new Blockbax Errors
def http_error_handler(r: requests.Response):
    raise_for_unauthorized_error(r, response_codes=[401])
    raise_client_error(r, [400, 402, 403] + list(range(405, 499)))
    raise_server_error(r, list(range(500, 600)))


def notify_partial_accepted(r: requests.Response, response_codes):
    # when sending measurements ingestion ID('s) could be rejected.
    # API returns a 207 with a message telling the user which ingestion ID('s) are not accepted.
    if r.status_code in response_codes:
        logger.warn(f"{json.loads(r.text)['message']}")


def notify_not_found(r: requests.Response, response_codes):
    if r.status_code in response_codes:
        logger.warn(
            f"Request with Url: {r.request.url} {(f', and body: {r.request.body}' if r.request.body else '')}, was not found!{(f', response: {r.text}' if r.text else '')}"
        )


def raise_client_error(r: requests.Response, response_codes: List[int]):
    try:
        r.raise_for_status()
    except requests.models.HTTPError as http_error:
        if r.status_code in response_codes:
            error_message_4xx = f"HTTP Error: {http_error}{(f', response: {r.text}' if r.text else '')}{(f', request body: {r.request.body}' if r.request.body else '')}"
            logger.error(error_message_4xx)
            raise errors.BlockbaxClientError(error_message_4xx)


def raise_server_error(r: requests.Response, response_codes: List[int]):
    try:
        r.raise_for_status()
    except requests.models.HTTPError as http_error:
        if r.status_code in response_codes:
            # with a 5xx there is no pint in trying to access the response content
            error_message_5xx = f"HTTP Error: {http_error}{(f', request body: {r.request.body}' if r.request.body else '')}"
            logger.error(error_message_5xx)
            raise errors.BlockbaxServerError(error_message_5xx)


def raise_for_unauthorized_error(r: requests.Response, response_codes: List[int]):
    """checks authorization for access token and project ID raises if status code is 401"""
    try:
        r.raise_for_status()
    except requests.models.HTTPError as http_error:
        if r.status_code in response_codes:
            if "Authorization" not in r.request.headers:
                prefix_error_message = (
                    f", 'Authorization' header is missing. "  # not likely
                )
            else:
                prefix_error_message = (
                    f", the access token is unauthorized. "  # unauthorized access token
                )
            error_message = f"HTTP error: {http_error}" + (
                prefix_error_message
                if prefix_error_message
                else ", Unknown unauthorized error."
            )
            raise errors.BlockbaxUnauthorizedError(error_message)


class JSONEncoderWithDecimal(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
