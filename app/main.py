from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.api.router import router
from app.utils.my_redis import get_redis
from config import settings


app = FastAPI()

app.include_router(router)

origins = [
    # frontend sources here
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def get_dbs():
    postgres_engine = create_async_engine(settings.postgres_db_url, poolclass=NullPool)
    app.async_session_maker = sessionmaker(postgres_engine, class_=AsyncSession, expire_on_commit=False)


@app.on_event('shutdown')
async def shutdown_event():
    redis = get_redis()
    await redis.aclose()
