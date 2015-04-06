import json
from unittest import TestCase
from test_util import create_mem_db
from over_achiever.models import metadata
from over_achiever.api import create_app
import over_achiever.models as m


class OverAchieverTest(TestCase):
    def setUp(self):
        self.app = create_app()
        self.session = create_mem_db(metadata, self.app.db)
        self.test_app = self.app.test_client()

        # add users
        u1 = m.User(name='user-1',
                    email='user-1@example.org',
                    password='123')
        u2 = m.User(name='user-2',
                    email='user-2@example.org',
                    password='123')

        self.user = m.User(name='user-3',
                           email='user-3@example.org',
                           password='123')

        self.session.add(u1)
        self.session.add(u2)
        self.session.add(self.user)

        # add goals
        goals = [None] * 8
        goals[0] = m.Goal(user=u1, name='goal-0')
        goals[1] = m.Goal(user=u1, name='goal-1')
        goals[2] = m.Goal(user=u1, name='goal-2', parent=goals[1])
        goals[3] = m.Goal(user=u1, name='goal-3', parent=goals[1])
        goals[4] = m.Goal(user=u1, name='goal-4', parent=goals[3])
        goals[5] = m.Goal(user=u1, name='goal-5', parent=goals[3])
        goals[6] = m.Goal(user=u1, name='goal-6', parent=goals[3])
        goals[7] = m.Goal(user=u2, name='goal-7')

        for g in goals:
            self.session.add(g)

        self.session.commit()

    def tearDown(self):
        pass

    def test_get_goals(self):
        #q = self.session.query

        url = '/v1.0/goals'
        response = self.test_app.get(url)
        result = json.loads(response.data)
        expected = {'user-1':
                        {'goal-0': {},
                         'goal-1':
                             {'goal-2': {},
                              'goal-3': {
                                'goal-4': {},
                                'goal-5': {},
                                'goal-6': {}}}},
                    'user-2':
                        {'goal-7': {}},
                    'user-3': {}}
        self.assertEqual(expected, result)

    def test_add_new_goal(self):
        q = self.session.query
        name = 'new-goal'
        # verify the goal doesn't exist yet
        self.assertIsNone(q(m.Goal).filter_by(name=name).scalar())

        params = dict(user=self.user.name,
                      name=name)
        url = '/v1.0/goals'
        response = self.test_app.post(url, data=params)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(q(m.Goal).filter_by(name=name).scalar())

    def test_add_nested_goals(self):
        q = self.session.query
        name = 'new-goal'
        # verify the goal doesn't exist yet
        self.assertIsNone(q(m.Goal).filter_by(name=name).scalar())

        params = dict(user=self.user.name,
                      name=name)
        url = '/v1.0/goals'
        response = self.test_app.post(url, data=params)
        self.assertEqual(200, response.status_code)
        parent_goal = q(m.Goal).filter_by(name=name).one()

        child_name = 'child'
        params = dict(user=self.user.name,
                      name=child_name,
                      parent_name=parent_goal.name)
        response = self.test_app.post(url, data=params)
        self.assertEqual(200, response.status_code)
        child_goal = q(m.Goal).filter_by(name=child_name).one()
        self.assertEqual(child_name, child_goal.name)
        self.assertEqual(parent_goal, child_goal.parent)

    def test_complete_goal(self):
        q = self.session.query
        params = dict(user='user-1',
                      name='goal-0')
        url = '/v1.0/goals'
        response = self.test_app.put(url, data=params)
        self.assertEqual(200, response.status_code)

        goal = q(m.Goal).filter_by(name='goal-0').one()
        self.assertIsNotNone(goal.end)

