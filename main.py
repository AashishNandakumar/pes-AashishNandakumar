from fastapi import FastAPI
from src.routers import database
from src.models import models
from src.db_config import engine

app = FastAPI(
    title="Google Sheets and Database Sync API",
    description="API for syncing Google Sheets data with a database and vice versa.",
    version="0.1.0",
)

app.include_router(database.router)

models.Base.metadata.create_all(engine)
