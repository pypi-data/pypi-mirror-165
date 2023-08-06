import json

import pytest
from google.protobuf import json_format

from aylien_model_serving.app_factory import FlaskAppWrapper
import test.example_schema_pb2 as schema


def predict(title=None, body=None, **kwargs):
    return {
        'language': 'en',
        'confidence': 0.71,
        'error': 'Not an error',
        'version': '0.0.1'
    }


def process_request():
    return FlaskAppWrapper.process_json(predict, schema=schema)


@pytest.fixture(scope="session", autouse=True)
def client():
    routes = [{"endpoint": "/", "callable": process_request, "methods": ["POST"]}]
    test_app = FlaskAppWrapper.create_app(routes)
    test_client = test_app.test_client()
    return test_client


def test_create_app():
    instance1 = FlaskAppWrapper()
    instance2 = FlaskAppWrapper()
    instance3 = FlaskAppWrapper()
    assert instance1 != instance2 != instance3
    assert instance1.app == instance2.app == instance3.app


def test_create_multiple_app():
    app1 = FlaskAppWrapper.create_app()
    app2 = FlaskAppWrapper.create_app()
    app3 = FlaskAppWrapper.create_app()
    assert app1 == app2 == app3


def post_json(client, url, json_dict):
    """Send dictionary json_dict as json to the specified url"""
    return client.post(url, data=json.dumps(json_dict), content_type="application/json")


def test_client_works(client):
    response = client.get("/__ping")
    assert b"Success" in response.data


def test_post_json_valid_req(client):
    payload = {
        "body": "This is a sentence",
        "title": "Title1",
        "enrichments": {
            "extracted": {
                "value": None
            }
        }
    }
    response = post_json(client, "/", payload)
    assert response.status_code == 200
    resp_json = response.json
    assert resp_json["error"] == "Not an error"
    assert resp_json["version"] == "0.0.1"


def test_post_json_invalid_req(client):
    response = post_json(client, "/", {"body": "This is a sentence", "language": "en"})
    assert response.status_code == 400
    resp_json = response.json
    assert '"app.Request" has no field named "language"' in resp_json["error"]


def test_protobuf_message_parsing(client):
    payload = {
        "abcd": "This is a sentence",
        "who": "I like sandwiches",
        "language": "en"
    }
    req_msg = schema.Request()
    msg = FlaskAppWrapper.parse_to_protobuf_msg(
        payload,
        req_msg,
        ignore_unknowns=True
    )
    assert msg.title == ''
    assert msg.body == ''

    error = False
    try:
        FlaskAppWrapper.parse_to_protobuf_msg(
            payload,
            req_msg,
            ignore_unknowns=False
        )
    except json_format.ParseError:
        error = True
    assert error, 'parsing should fail when ignore_unknowns=False'


def test_metrics(client):
    """
    Do not test actual metrics here - this will vary based on HW ,
    and might give different results on jenkins
    """
    response = client.get("/__metrics")
    data = str(response.data)
    assert "flask_http_request_duration_seconds_bucket" in data
    assert "flask_http_request_created" in data
    assert "flask_http_request_duration_seconds_count" in data
    assert "flask_http_request_duration_seconds_created" in data
