"""
/llrws/__init__.py

Concerns all things LLR Web Suite.
"""

from flask import Flask
from flask_restful import Api

from llrws.config import Config
from llrws.api.routes import initialize_routes

application = Flask(__name__)


def create_app(config_class=Config):
    """Creates Flask application instance."""
    application.config.from_object(config_class)

    from llrws.api.routes import api_bp

    api = Api(api_bp)
    initialize_routes(api)

    application.register_blueprint(api_bp, subdomain="api")

    return application
