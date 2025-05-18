from flask import Flask
from flasgger import Swagger
from .config import Config
from .extensions import db, ma, jwt
from .routes.auth import auth_bp
from .routes.posts import posts_bp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        origins="https://md-editor-frontend.vercel.app",
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    template = {
        "swagger": "2.0",
        "info": {
            "title": "MD Editor API",
            "version": "1.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT como: Bearer {token}"
            }
        },
        "definitions": {
            "Post": {
                "type": "object",
                "properties": {
                    "id":         {"type": "integer"},
                    "title":      {"type": "string"},
                    "content":    {"type": "string"},
                    "user_id":    {"type": "integer"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        }
    }
    swagger_config = {
        'headers': [],
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/apispec.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True
            }
        ],
        'static_url_path': '/flasgger_static',
        'swagger_ui': True,
        'specs_route': '/docs/'
    }
    Swagger(app, config=swagger_config, template=template)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(posts_bp, url_prefix="/posts")

    return app
