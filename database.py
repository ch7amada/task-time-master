from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

"""
- Define database url
- connect to database using sqlalchemy
- small function for getting database later in the api routes
"""

DATABASE_URL = "sqlite:///./data/timesheet.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} # need for sqlite
)

SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()