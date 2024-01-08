from sqlalchemy import Column, String, Integer, Boolean

from app.utils.base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    is_verified = Column(Boolean, default=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
