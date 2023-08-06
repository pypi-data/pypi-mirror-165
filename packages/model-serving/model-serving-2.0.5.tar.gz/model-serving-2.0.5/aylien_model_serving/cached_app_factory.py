import json

from flask import request, copy_current_request_context
from flask_caching import Cache

from aylien_model_serving.app_factory import FlaskAppWrapper


def cache_key():
    @copy_current_request_context
    def my_key():
        return json.dumps(request.get_json())

    return my_key()


class CachedFlaskAppWrapper:
    """specify a new app here -
    it gives the option to override app config specifically for cached apps"""

    cache = Cache()

    @staticmethod
    @cache.cached(key_prefix=cache_key)
    def process_json(callable_handler):
        return FlaskAppWrapper.process_json(callable_handler)

    @staticmethod
    def create_app(routes=None, cache_config=None):
        app = FlaskAppWrapper.create_app(routes)
        if cache_config is None:
            cache_config = {
                "CACHE_TYPE": "SimpleCache",
                "CACHE_THRESHOLD": 100000
            }
        CachedFlaskAppWrapper.cache.init_app(app, cache_config)
        return app
