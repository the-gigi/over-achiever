from datetime import datetime
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

import models as m


db = None


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


class Goal(Resource):
    def get(self):
        """Get all goals organized by user and in hierarchy"""
        q = db.session.query
        result = {}
        users = q(m.User).all()
        for u in users:
            result[u.name] = _get_goal_tree(q, u)

        return result

    def post(self):
        parser = RequestParser()
        parser.add_argument('user', type=str, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('parent_name', type=str)
        parser.add_argument('description', type=str, required=False)
        args = parser.parse_args()

        # Get a SQL Alchemy query object
        q = db.session.query

        # Create a new goal
        user = q(m.User).filter_by(name=args.user).one()

        # Find parent goal by name
        if args.parent_name:
            parent = q(m.Goal).filter_by(name=args.parent_name).one()
        else:
            parent = None

        goal = m.Goal(user=user,
                      parent=parent,
                      name=args.name,
                      description=args.description)

        db.session.add(goal)
        db.session.commit()

    def put(self):
        """Update end time"""
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()

        # Get a SQL Alchemy query object
        q = db.session.query
        goal = q(m.Goal).filter_by(name=args.name).one()
        goal.end = datetime.now()

        db.session.commit()


