from aylien_model_serving.cached_app_factory import CachedFlaskAppWrapper
from .example_serving_handler import predict


def process_request():
    return CachedFlaskAppWrapper.process_json(predict)


def run_app():
    routes = [{"endpoint": "/",
               "callable": process_request,
               "methods": ["POST"]}]
    cache_config = {
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": "./cache",
        "CACHE_DEFAULT_TIMEOUT": 300,
    }
    return CachedFlaskAppWrapper.create_app(routes, cache_config)
