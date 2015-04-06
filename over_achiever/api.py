import os
from flask import Flask
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from resources import User, Goal
import resources


def create_app():
    app = Flask(__name__)
    app.config.from_object('over_achiever.config')
    resources.db = app.db = SQLAlchemy(app)
    api = Api(app)
    resource_map = (
        (User, '/v1.0/users'),
        (Goal, '/v1.0/goals'),
    )

    for resource, route in resource_map:
        api.add_resource(resource, route)

    return app

the_app = create_app()

if __name__ == "__main__":
    print("If you run locally, browse to localhost:5000")
    host = '0.0.0.0'
    port = int(os.environ.get("PORT", 5000))
    the_app.run(host=host, port=port)
