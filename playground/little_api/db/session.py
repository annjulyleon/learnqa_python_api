from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URI = "sqlite:///example.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False} #required for sqlite
)

# session is orm specific, main point of access to database in orm
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)