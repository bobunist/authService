from abc import ABC, ABCMeta, abstractmethod
from datetime import timedelta

from app.utils.uow import IUnitOfWork
from app.schemas.user import *


class IAuthService(ABC):
    __metaclass__ = ABCMeta
    _uow: IUnitOfWork

    @abstractmethod
    def _generate_confirm_code(self):
        raise NotImplementedError

    @abstractmethod
    async def reg_user(self, user: UserReg, uow: IUnitOfWork):
        raise NotImplementedError

    @abstractmethod
    async def confirm_reg(self, email: str, confirm_code: str, uow: IUnitOfWork):
        raise NotImplementedError

    @abstractmethod
    def _hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        raise NotImplementedError

    @abstractmethod
    async def log_user(self, email: str, password: str, uow: IUnitOfWork) -> dict:  # return token
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_id: int, uow: IUnitOfWork) -> UserRead | None:
        raise NotImplementedError
