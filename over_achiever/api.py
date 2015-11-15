import os

from flask import Flask, url_for, session, request, jsonify
from flask.ext.oauthlib.client import OAuth
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api, abort
import models
import resources
from resources import User, Goal


def create_app():
    app = Flask(__name__)
    app.config.from_object('over_achiever.config')
    db = SQLAlchemy(app, metadata=models.metadata)
    db.create_all()
    resources.db = app.db = db

    # app.secret_key = 'you-will-never-guess' # should get it from config
    oauth = OAuth(app)

    github = oauth.remote_app(
        'github',
        consumer_key='a11a1bda412d928fb39a',
        consumer_secret='92b7cf30bc42c49d589a10372c3f9ff3bb310037',
        request_token_params={'scope': 'user:email'},
        base_url='https://api.github.com/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize'
    )

    # set the token getter for the auth client
    github._tokengetter = lambda: session.get('github_token')
    resources.github = app.github = github

    api = Api(app)
    resource_map = (
        (User, '/v1.0/users'),
        (Goal, '/v1.0/goals'),
    )

    for resource, route in resource_map:
        api.add_resource(resource, route)

    return app

app = create_app()


@app.route('/login')
def login():
    return app.github.authorize(callback=url_for('authorized',
                                                 _external=True))


@app.route('/logout')
def logout():
    session.pop('github_token', None)


@app.route('/login/authorized')
def authorized():
    resp = app.github.authorized_response()
    if resp is None:
        # return 'Access denied: reason=%s error=%s' % (
        #     request.args['error'],
        #     request.args['error_description']
        # )
        abort(401, message='Access denied!')
    session['github_token'] = (resp['access_token'], '')
    user = app.github.get('user')
    return jsonify(user.data)

# @app.github.tokengetter
# def get_github_oauth_token():
#     return session.get('github_token')

if __name__ == "__main__":
    print("If you run locally, browse to localhost:5000")
    host = '0.0.0.0'
    port = int(os.environ.get("PORT", 5000))
    app.run(host=host, port=port)
