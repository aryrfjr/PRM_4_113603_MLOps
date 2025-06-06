from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

#######################################################################
#
# DB session and engine with SQLAlchemy, for working with the DB using
# Object-Relational Mapping (ORM) as well as direct SQL execution
#
#######################################################################

# NOTE: the DATABASE_URL environment variable was defined in docker-compose.yml
DATABASE_URL = os.getenv("DATABASE_URL")


#
# SQLAlchemy 2.0 Declarative Base (shared with models.py)
#
# NOTE: The Base class acts as a common ancestor for all ORM model
#   classes (i.e., tables). Any class that inherits from Base will
#   automatically be mapped to a table in the database.
#
#######################################################################
class Base(DeclarativeBase):
    pass  # this class itself doesn't add any extra behavior; it's just defining the base


# The SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL, echo=False, future=True  # Set to True for SQL query logging
)

# SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


# Dependency for FastAPI routes (ensuring session cleanup)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
