from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import os

engine = create_engine(os.getenv('DATABASE_URL'))
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        Session.remove()