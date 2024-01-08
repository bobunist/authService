from datetime import timedelta, datetime
import random

from celery import Task
from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from app.schemas.user import UserAuth, UserRead, User, UserReg
from app.services.auth.celery_tasks import send_email_confirm
from app.utils.uow import IUnitOfWork
from config import settings


class AuthService(Task):

    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._incorrect_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        self._incorrect_confirm_code = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect confirm code",
            headers={"WWW-Authenticate": "Bearer"},
        )
        self._confirm_code_expire = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect confirm code",
            headers={"WWW-Authenticate": "Bearer"},
        )
        self._confirm_error = HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already verified or doesn't exist."
            )

    def _generate_confirm_code(self):
        confirm_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        return confirm_code

    async def confirm_reg(self, email: str, confirm_code: str, uow: IUnitOfWork):
        async with uow:
            existed_user = await uow.user.get_one(email=email)
            existed_user = User.model_validate(existed_user)
            if not existed_user or existed_user.is_verified:
                raise self._confirm_error

            right_confirm_code = await uow.redis.get(email)

            if not right_confirm_code:
                raise self._confirm_code_expire

            right_confirm_code = right_confirm_code.decode('utf-8')

            if right_confirm_code == confirm_code:
                user = await uow.user.get_one(email=email)
                user = User.model_validate(user)
                user.is_verified = True
                await uow.user.update_one(user.id, user.model_dump())
            else:
                raise self._incorrect_confirm_code

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(password, hashed_password)

    def _hash_password(self, password: str) -> str:
        hashed_password = self._pwd_context.hash(password)
        return hashed_password

    def _create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    async def send_email_confirm(self, email_address, uow: IUnitOfWork):
        async with uow:
            existed_user = await uow.user.get_one(email=email_address)
            existed_user = User.model_validate(existed_user)
            if not existed_user or existed_user.is_verified:
                raise self._confirm_error

            send_email_confirm.apply_async(args=[email_address])

    async def reg_user(self, user: UserAuth, uow: IUnitOfWork):
        async with uow:
            existed_user = await uow.user.get_one(email=user.email)
            if existed_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='Email is busy'
                )
            hashed_password = self._hash_password(user.password)
            user_reg = UserReg(email=user.email, hashed_password=hashed_password)

            await uow.user.add_one(user_reg.model_dump())
            access_token_expires = timedelta(minutes=int(settings.access_token_expire_minutes))
            access_token = self._create_access_token(
                data={"sub": user.email}, expires_delta=access_token_expires
            )

            send_email_confirm.apply_async(args=[user.email])

            return {"access_token": access_token, "token_type": "bearer"}

    async def log_user(self, email: str, password: str, uow: IUnitOfWork) -> dict:
        async with uow:
            user_from_db = await uow.user.get_one(email=email)
            if not user_from_db:
                raise self._incorrect_error
            user_from_db = User.model_validate(user_from_db)
            hashed_password = user_from_db.hashed_password
            password = password
            if self._verify_password(password, hashed_password):
                access_token_expires = timedelta(minutes=int(settings.access_token_expire_minutes))
                access_token = self._create_access_token(
                    data={"sub": email}, expires_delta=access_token_expires
                )
                return {"access_token": access_token, "token_type": "bearer"}
            raise self._incorrect_error

    async def get_me(self, email: str, uow: IUnitOfWork) -> UserRead | None:
        async with uow:
            user = await uow.user.get_one(email=email)
            user = UserRead.model_validate(user)
            return user

    async def get_user(self, uow: IUnitOfWork, **kwargs) -> UserRead | None:
        async with uow:
            user = await uow.user.get_one(**kwargs)
            if not user:
                return
            user = UserRead.model_validate(user)
            return user
