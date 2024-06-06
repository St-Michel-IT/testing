import asyncio
import json

import bleak as bleak
import pytest
import requests
from werkzeug.test import Client

# The event loop is needed to run the coroutine
loop = asyncio.get_event_loop()

# The scanner object is used to discover BLE devices
scanner = bleak.BleakScanner()
from ble_to_rpc import application

SCAN_CALL = {
    "method": "scan",
    "params": [],
    "jsonrpc": "2.0",
    "id": 0,
}
URL = "http://localhost:4000/jsonrpc"


def get_executed_coroutine_discover():
    """
    BleakScanner.discover() is a coroutine, so we need to run it in an event
    loop.

       :return: The only result of the coroutine, a list of BLEDevice
          objects address as strings.
    """
    result = loop.run_until_complete(
        asyncio.gather(
            scanner.discover()
        )
    )[0]
    # turn all BLEDevice objects into dictionaries
    return [device.address for device in result]


@pytest.fixture()
def post(request) -> requests.Response:
    return requests.post(URL, json=SCAN_CALL)


@pytest.mark.parametrize("post", [{"method": "scan", "args": []}, ], indirect=True)
def test_is_json(post):
    """
    Test the JSON response can be loaded.
    :param post: Fixture of the scan call
    """
    try:
        json.loads(post.text)
    except json.JSONDecodeError as e:
        pytest.fail("Not a JSON response : %s" % e)


@pytest.mark.parametrize("post", [{"method": "scan", "args": []}], indirect=True)
def test_is_rpc(post):
    """
    Test the JSON response can be loaded.
    :param post: Fixture of the scan call
    """
    assert post.json().get("jsonrpc") == "2.0", "Not a JSON RPC response"


@pytest.mark.parametrize("post", [{"method": "scan", "args": []}], indirect=True)
def test_is_http_ok(post):
    """
    Test the JSON response can be loaded.
    :param post: Fixture of the scan call
    """
    assert post.status_code == 200


WRONG_PATHS = ["ksbhv", "kslijvk", "lnklk"]


@pytest.mark.parametrize("path,", WRONG_PATHS)
def test_get_wrong_path(path):
    """
    Test the JSON response can be loaded.
    :param path: Wrong paths list
    """
    url = "http://localhost:4000/%s" % path
    r = requests.get(url)
    assert r.status_code == 404


@pytest.mark.parametrize("path,", WRONG_PATHS)
def test_post_wrong_path(path):
    """
    Test the JSON response can be loaded.
    :param path: Wrong paths list
    """
    url = "http://localhost:4000/%s" % path
    r = requests.get(url)
    assert r.status_code == 404


@pytest.mark.parametrize("post", [{"method": "son", "args": []}], indirect=True)
def test_wrong_method(post):
    """
    Test the JSON response can be loaded.
    :param post: Fixture of the scan call
    """
    assert post.status_code == 200


@pytest.mark.parametrize("post", [{"method": "scan", "args": []}], indirect=True)
def test_is_ble_ok(post):
    """
    Test the JSON response can be loaded.
    :param post: Fixture of the scan call
    """
    response_result = post.json()["result"]
    bleak_result = get_executed_coroutine_discover()
    check = all(response_result in post.json()["result"] for e in bleak_result)
    if check is False:
        pytest.fail("Wrong addres in the response")


@pytest.fixture(scope="module")
def werkzeug_app_client():
    return Client(application)


def test_is_werkzeug_ok(werkzeug_app_client):
    """
    Test the JSON response can be loaded.
    :param werkzeug_app_client: Fixture of the scan call
    """
    response = werkzeug_app_client.post(
        "/jsonrpc", data=json.dumps(SCAN_CALL), content_type="application/json"
    )
    assert response.status_code == 200
    assert response.json.get("jsonrpc") == "2.0", "Not a JSON RPC response"


SCAN_CALL_NO_ID = {
    "method": "scan",
    "params": [],
    "jsonrpc": "2.0",
}


def test_is_http_ko_no_id_with_client(werkzeug_app_client):
    """
    Test the JSON response can be loaded.
    :param post: Fixture of the scan call
    """
    with pytest.raises(AttributeError):
        response = werkzeug_app_client.post(
            "/jsonrpc",
            data=json.dumps(SCAN_CALL_NO_ID), content_type="application/json"
        )
        assert response.status_code == 500


def test_is_http_ko_no_id_with_requests():
    """
    Test the JSON response can be loaded.
    :param post: Fixture of the scan call
    """
    response = requests.post(
        URL,
        json=SCAN_CALL_NO_ID
    )
    assert response.status_code == 500
