from typing import List

from sqlalchemy import insert, select, update, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.repositories.i_repo import IRepository


class Repository(IRepository):
    model: DeclarativeBase = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar()

    async def add_some(self, data: List[dict]):
        stmt = insert(self.model).values(data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_one(self, **kwargs):
        stmt = select(self.model).filter_by(**kwargs)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_some(self, **kwargs) -> List:
        stmt = select(self.model).filter_by(**kwargs)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_some_with_sqlalchemy_stmt(self, stmt):
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_all(self, page: int = 1, items_per_page: int = 10):
        total_count = await self.session.scalar(select(func.count()).select_from(self.model))

        stmt = select(self.model).order_by(self.model.id)
        stmt = stmt.limit(items_per_page).offset((page - 1) * items_per_page)
        res = await self.session.execute(stmt)

        return {"count": total_count, "items": res.scalars().all()}

    async def update_one(self, id, data: dict):
        stmt = update(self.model).where(self.model.id == id).values(data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update_some(self, stmt, data: dict):
        stmt = update(self.model).values(**data).where(stmt).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def delete_one(self, stmt):
        stmt = delete(self.model).where(stmt).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete_some(self, stmt) -> List:
        stmt = delete(self.model).where(stmt).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalars().all()
