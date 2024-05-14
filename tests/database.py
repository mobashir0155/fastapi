from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
from app.database import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
alembic_cfg = Config("alembic.ini")

@pytest.fixture()
def session():
    command.upgrade(config=alembic_cfg,revision="head")
    
    db = TestSessionLocal()
    try:
        yield db
    finally:
        command.downgrade(config=alembic_cfg,revision="base")
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        db = TestSessionLocal()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
