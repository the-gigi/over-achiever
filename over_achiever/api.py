from flask import Flask, url_for, session, jsonify
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, abort
from . import models
from . import resources
from .resources import User, Goal


def create_app():
    app = Flask(__name__)
    app.config.from_object('over_achiever.config')
    db = SQLAlchemy(app, metadata=models.metadata)
    db.create_all()
    resources.db = app.db = db

    oauth = OAuth(app)
    github = oauth.remote_app(
        'github',
        consumer_key='507e57ab372adeb8051b',
        consumer_secret='08a7dbaa06ac16daab00fac53724ee742c8081c5',
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
    callback = url_for('authorized', _external=True)
    return app.github.authorize(callback)


@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return 'OK'


@app.route('/login/authorized')
def authorized():
    resp = app.github.authorized_response()
    if resp is None:
        # return 'Access denied: reason=%s error=%s' % (
        #     request.args['error'],
        #     request.args['error_description']
        # )
        abort(401, message='Access denied!')
    token = resp['access_token']
    # Must be in a list or tuple because github auth code extracts the first
    user = app.github.get('user', token=[token])
    user.data['access_token'] = token
    return jsonify(user.data)
