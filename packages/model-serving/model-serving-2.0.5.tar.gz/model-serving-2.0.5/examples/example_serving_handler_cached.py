from aylien_model_serving.cached_app_factory import CachedFlaskAppWrapper
from .example_serving_handler import predict


def process_request():
    return CachedFlaskAppWrapper.process_json(predict)


def run_app():
    routes = [{"endpoint": "/",
               "callable": process_request,
               "methods": ["POST"]}]
    return CachedFlaskAppWrapper.create_app(routes)
