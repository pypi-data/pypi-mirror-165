from aylien_model_serving.cached_app_factory import CachedFlaskAppWrapper
import pytest
import json

counter = 0


def process_response(**kwargs):
    global counter
    counter += 1
    return {}


@pytest.fixture
def client():
    routes = [{"endpoint": "/cached", "callable": process_request_cached, "methods": ["POST"]}]
    test_app = CachedFlaskAppWrapper.create_app(routes)
    client = test_app.test_client()

    return client


def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url"""
    return client.post(url, data=json.dumps(json_dict), content_type="application/json")


def process_request_cached():
    return CachedFlaskAppWrapper.process_json(process_response)


def test_cache_hit_and_miss(client):
    post_json(client, "/cached", {"body": "This is a sentence"})
    post_json(client, "/cached", {"body": "This is a sentence"})
    assert 1 == counter  # cache hit
    client.post("/cached", json={"index_id": "", "query": "I am shark"})
    assert 2 == counter  # cache miss


def test_metrics(client):
    response = client.get("/__metrics")
    data = str(response.data)
    assert "flask_http_request_duration_seconds_bucket" in data
    assert "flask_http_request_created" in data
    assert "flask_http_request_duration_seconds_count" in data
    assert "flask_http_request_duration_seconds_created" in data


def test_client_works(client):
    response = client.get("/__ping")
    assert b"Success" in response.data
