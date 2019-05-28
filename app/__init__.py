#!/usr/bin/env python3
from flask import Flask
from flask_pymongo import PyMongo
from flask_talisman import Talisman
from app.config import Config

mongo = PyMongo()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    mongo.init_app(app)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    from app.users.routes import users
    from app.main.routes import main
    from app.recipes.routes import recipes
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(recipes)

    csp = {
        'default-src': [
            '\'unsafe-inline\' \'self\'',
            '*.cloudflare.com',
            '*.fontawesome.com',
            '*.googleapis.com',
            '*.gstatic.com'
        ],
        'img-src': '*',
        'script-src': [
            '\'unsafe-inline\' \'self\'',
            '*.cloudflare.com',
            '*.fontawesome.com',
            '*.googleapis.com',
            '*.gstatic.com'
        ]
    }

    Talisman(app, content_security_policy=csp)

    return app
