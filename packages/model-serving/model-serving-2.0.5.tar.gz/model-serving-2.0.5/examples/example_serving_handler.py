import examples.example_schema_pb2 as schema
from aylien_model_serving.app_factory import FlaskAppWrapper, InvalidRequest


def predict_lang(text):
    return "en", 0.71


def predict(title=None, body=None, enrichments=None):
    if body is None:
        body = enrichments["extracted"]["value"]["body"]
    if title is None and body is None:
        raise InvalidRequest("Missing text")
    article_text = f"{title} {body}"
    detected_lang, confidence = predict_lang(article_text)
    return {
        'language': detected_lang,
        'confidence': confidence,
        'error': 'Not an error',
        'version': '0.0.1'
    }


def process_request():
    return FlaskAppWrapper.process_json(predict, schema=schema)


def run_app():
    routes = [
        {
            "endpoint": "/",
            "callable": process_request,
            "methods": ["POST"]
        }
    ]
    return FlaskAppWrapper.create_app(routes)
