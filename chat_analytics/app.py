
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_restx import Api
from chat_analytics.api.health import ns as health_ns
from chat_analytics.api.conversation_analyzer import ns as conversation_analyzer_ns


def create_app():
    app = Flask(__name__)
    CORS(app, resource={r"/*": {"origins": "*"}})
    health_blueprint = Blueprint("chat-analytics-health", __name__)
    v1_blueprint = Blueprint("chat-analytics", __name__, url_prefix="/v1")
    api_health = Api(
        health_blueprint,
        title="chat-analytics API Health",
        description="non-versioned health check, see /v1 for versioned api",
    )
    api_v1 = Api(v1_blueprint, title="Chat Analytics API", version="1.0", description="Chat Analytics API")
    api_health.add_namespace(health_ns)
    api_v1.add_namespace(conversation_analyzer_ns)
    app.register_blueprint(v1_blueprint)
    app.register_blueprint(health_blueprint)

    return app
