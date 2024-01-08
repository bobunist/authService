from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def add_some(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_some(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id, data):
        raise NotImplementedError

    @abstractmethod
    async def update_some(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_some(self, **kwargs):
        raise NotImplementedError
