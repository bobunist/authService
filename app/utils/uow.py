from abc import ABC, abstractmethod

from redis.asyncio import Redis

from app.repositories.i_repo import IRepository
from app.repositories.user_repository import UserRepository
from app.utils.async_session_maker import get_async_session_maker
from app.utils.my_redis import get_redis


class IUnitOfWork(ABC):
    user: IRepository
    redis: Redis

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def flush(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = get_async_session_maker()
        self.redis = get_redis()

    async def __aenter__(self):
        self.session = self.session_factory()

        self.user = UserRepository(self.session)

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def flush(self):
        await self.session.flush()

    async def rollback(self):
        await self.session.rollback()
