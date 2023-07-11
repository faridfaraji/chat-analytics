
from flask import Blueprint, Flask
from flask_restx import Api
from template.api.health import ns as health_ns


def create_app():
    app = Flask(__name__)
    health_blueprint = Blueprint("template-health", __name__)
    api_health = Api(
        health_blueprint,
        title="Template API Health",
        description="non-versioned health check, see /v1 for versioned api",
    )
    api_health.add_namespace(health_ns)
    app.register_blueprint(health_blueprint)
    return app
