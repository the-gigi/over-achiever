# -*- coding: utf8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
                                                      'over_acheiver.db')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# mail server settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# administrator list
ADMINS = ['']

# pagination
POSTS_PER_PAGE = 3


# Enable DB query timing
SQLALCHEMY_RECORD_QUERIES = True
# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5
