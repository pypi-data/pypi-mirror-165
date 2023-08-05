from datetime import datetime
import functools
import sys
import xml.etree.ElementTree as ET

from json import JSONDecodeError

from .exceptions import SdkException
from requests import RequestException, Response


def handle_data_store_response(response):
    """Return the content of a response received from the datastore
    or parse the send error and raise it.

    Args:
        response (requests.Response): A response from the data store.

    Raises:
        SdkException: When the response contains an error.

    Returns:
        :obj:`str`: Content of the response.
    """
    if 200 <= response.status_code < 300:
        return response.content

    # Parse XML error returned by the data store before raising it
    xml_error_node = ET.fromstring(response.text)
    error_infos = {node.tag: node.text for node in xml_error_node}
    error_code = error_infos.pop("Code")
    error_message = error_infos.pop("Message")
    raise SdkException(
        message=error_message,
        status_code=response.status_code,
        name=error_code,
        additional_data=error_infos,
    )


def _parse_json_response(response):
    if response.status_code == 204 or response.text == "OK":
        return
    try:
        response_json = response.json()
    except JSONDecodeError as error:
        raise SdkException(
            f"Unable to decode response data into json. Data being:\n'{response.text}'"
        ) from error
    return response_json


def _raise_craft_ai_error_from_response(response: Response):
    try:
        error_content = response.json()
        raise SdkException(
            message=error_content["message"],
            status_code=response.status_code,
            name=error_content.get("name"),
            stack_message=error_content.get("stackMessage"),
            request_id=error_content.get("requestId"),
            additional_data=error_content.get("additionalData"),
        )
    except JSONDecodeError as error:
        raise SdkException(
            "The server returned invalid response", status_code=response.status_code
        ) from error


def handle_http_request(request_func):
    def wrapper(*args, **kwargs):
        try:
            response = request_func(*args, **kwargs)
        except RequestException as error:
            raise SdkException(
                "Unable to perform the request", name="RequestError"
            ) from error

        if 200 <= response.status_code < 300:
            return _parse_json_response(response)
        _raise_craft_ai_error_from_response(response)

    return wrapper


def log_action(sdk, message):
    if sdk.verbose_log:
        print(message, file=sys.stderr)


def log_func_result(message):
    def decorator_log_func_result(action_func):
        @functools.wraps(action_func)
        def wrapper_log_func_result(*args, **kwargs):
            sdk = args[0]
            try:
                res = action_func(*args, **kwargs)
                log_action(sdk, "{:s} succeeded".format(message))
                return res
            except SdkException as error:
                log_action(sdk, "{:s} failed ! {}".format(message, error))
                raise error
            except Exception as error:
                log_action(
                    sdk, "{:s} failed for unexpected reason ! {}".format(message, error)
                )
                raise error

        return wrapper_log_func_result

    return decorator_log_func_result


def _datetime_to_timestamp_in_ms(dt):
    if not isinstance(dt, datetime):
        raise ValueError("Parameter must be a datetime.datetime object.")
    return int(1_000 * dt.timestamp())


def parse_isodate(date_string):
    """_summary_

    Args:
        date_string (str): date in ISO 8601 format potentially ending with
            "Z" specific character.

    Returns:
        :obj:`datetime.datetime`: A `datetime` corresponding to `date_string`.
    """
    return datetime.fromisoformat(date_string.rstrip("Z"))
