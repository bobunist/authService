from pydantic import BaseModel, Field, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field(default=None)
    is_verified: bool = Field(default=False)
    email: str = Field()
    hashed_password: str = Field()


class UserReg(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    is_verified: bool = Field(default=False)
    email: str = Field()
    hashed_password: str = Field()


class UserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str = Field()
    password: str = Field()


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field()
    is_verified: bool = Field()
    email: str = Field()
