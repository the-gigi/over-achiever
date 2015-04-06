from functools import partial
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


def create_mem_db(metadata, db):
    """Replace the Session class with an in-memory test Session class

    Very useful for fast and non-destructive tests (avoid hitting real DB)

    The operation is very tricky because it requires replacing and later
    restoring the engine in the guts of Flask-SQLAlchemy.

    The engine is accessible through a get_engine() method that must be
    replaced and later restored.

    To achieve that the object is viciously manipulated:

    1. the original get_engine() method is replaced with a lambda function that returns the in-memory engine
    2. a new method is added to the db object called restore_engine(). This method restored the original
       get_engine() method and deletes itself for good measure to leave the db object as pristine as it was before


    NOTE: must call db.restore_engine() in the tearDown() method of your test
    """

    def _restore_engine(self, original_get_engine):
        self.get_engine = original_get_engine
        delattr(self, 'restore_engine')

    engine = create_engine('sqlite:///:memory:',
                           echo=False,
                           connect_args={'check_same_thread': False},
                           poolclass=StaticPool)
    metadata.create_all(engine)
    original_get_engine = db.get_engine
    db.restore_engine = partial(_restore_engine, db, original_get_engine)
    db.get_engine = lambda x, y=None: engine
    session = db.create_scoped_session()

    return session




