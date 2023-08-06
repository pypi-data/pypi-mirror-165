import logging
import os

from flask import Flask, request, jsonify
from flask_api import status
from prometheus_flask_exporter import PrometheusMetrics
import google.protobuf.json_format as proto_json


class InvalidRequest(Exception):
    pass


class FlaskAppWrapper:
    app = Flask(__name__)
    metrics = PrometheusMetrics(app, group_by="endpoint", path="/__metrics")
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)
    logger.setLevel(os.environ.get("LOG_LEVEL", logging.WARNING))

    @staticmethod
    def parse_to_protobuf_msg(req_data, proto_msg, ignore_unknowns=False):
        return proto_json.ParseDict(
            req_data, proto_msg,
            ignore_unknown_fields=ignore_unknowns
        )

    @staticmethod
    def parse_proto_msg_to_json(
            response, preserve_field_name=True, include_defaults=True
    ):
        return proto_json.MessageToJson(
            response,
            preserving_proto_field_name=preserve_field_name,
            including_default_value_fields=include_defaults,
        )

    @staticmethod
    @metrics.do_not_track()
    def ping():
        return "Success", status.HTTP_200_OK

    @staticmethod
    def process_json(callable_handler, schema=None):
        response = {}
        try:
            req_data = request.get_json(force=True)
            if schema is not None:
                _ = FlaskAppWrapper.parse_to_protobuf_msg(
                    req_data, schema.Request())

            response = callable_handler(**req_data)

            if schema is not None:
                # back to protobuf to json
                _ = FlaskAppWrapper.parse_to_protobuf_msg(
                    response, schema.Response()
                )
            response_status = status.HTTP_200_OK
        except proto_json.Error as e:
            response["error"] = str(e)
            FlaskAppWrapper.logger.error(str(e))
            response_status = status.HTTP_400_BAD_REQUEST
        except InvalidRequest as e:
            response["error"] = str(e)
            FlaskAppWrapper.logger.error(str(e))
            response_status = status.HTTP_400_BAD_REQUEST
        except KeyError as e:
            response["error"] = str(e)
            FlaskAppWrapper.logger.error(str(e))
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        except Exception as e:
            response["error"] = str(e)
            FlaskAppWrapper.logger.error(str(e))
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        response = jsonify(response)
        response.status = response_status
        return response

    @staticmethod
    def create_app(routes=None):
        if routes is None:
            routes = []
        FlaskAppWrapper.app.add_url_rule(
            "/__ping", view_func=FlaskAppWrapper.ping,
            methods=["GET"]
        )
        for route in routes:
            FlaskAppWrapper.app.add_url_rule(
                route["endpoint"], view_func=route["callable"],
                methods=route["methods"]
            )  # is a list
        return FlaskAppWrapper.app
