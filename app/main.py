from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
# from . import models
# from .database import engine
from .routes import posts, users, auth, votes
from alembic.config import Config
from alembic import command

# config = context.config
# config.set_main_option("sqlalchemy.url",f"postgresql+psycopg2://{configs.database_username}:{configs.database_password}@{configs.database_hostname}:{configs.database_port}/{configs.database_name}")


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@asynccontextmanager
async def lifespan(app_: FastAPI):
    print("Starting up...")
    print("run alembic upgrade head...")
    run_migrations()
    yield
    print("Shutting down...")
# We are genrating schemas from alembic so no need ot add this line
# models.Base.metadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {"message": "Hello World"}



