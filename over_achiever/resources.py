from datetime import datetime

from flask import session
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

import models as m


db = None
github = None


def _get_session():
    return db.session


def _get_query():
    return _get_session().query


class User(Resource):
    def get(self):
        pass

    def post(self):
        pass


def _get_goals_by_parent(q, user, parent_goal):
    return q(m.Goal).filter_by(user=user, parent=parent_goal).all()


def _get_goal_tree(q, user, goal=None):
    """
    :param q: query
    :param user: user model
    :param goal: parent goal


    Populate recursively the goals array.
    """
    sub_goals = _get_goals_by_parent(q, user, goal)

    result = {}
    for g in sub_goals:
        result[g.name] = _get_goal_tree(q, user, g)

    return result


def _get_user():
    """Get the user object or create it based on the token in the session

    If there is no access token abort with 401 message
    """
    if 'github_token' not in session:
        abort(401, message='Access Denied!')

    user_data = github.get('user').data
    email = user_data['email']
    name = user_data['name']
    q = _get_query()
    user = q(m.User).filter_by(email=email).scalar()
    if not user:
        user = m.User(email=email, name=name)
        s = _get_session()
        s.add(user)

    return user

class Goal(Resource):
    def get(self):
        """Get all goals organized by user and in hierarchy

        If user doesn't exist create it (with no goals)
        """
        user = _get_user()
        q = _get_query()
        result = {user.name: _get_goal_tree(q, user)}

        return result

    def post(self):
        user = _get_user()
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('parent_name', type=str)
        parser.add_argument('description', type=str, required=False)
        args = parser.parse_args()

        # Get a SQL Alchemy query object
        q = _get_query()

        # Create a new goal

        # Find parent goal by name
        parent = q(m.Goal).filter_by(name=args.parent_name).scalar()

        goal = m.Goal(user=user,
                      parent=parent,
                      name=args.name,
                      description=args.description)

        s = _get_session()
        s.add(goal)

    def put(self):
        """Update end time"""
        user = _get_user()
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()

        # Get a SQL Alchemy query object
        q = _get_query()
        goal = q(m.Goal).filter_by(user=user, name=args.name).one()
        goal.end = datetime.now()



