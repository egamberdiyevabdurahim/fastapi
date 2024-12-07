from datetime import datetime, timezone

from pydantic import BaseModel, Field


class UsersIn(BaseModel):
    username: str = Field(max_length=100, min_length=3, unique=True, index=True)
    password : str = Field(max_length=50, min_length=8)
    email: str = Field(max_length=100, min_length=10)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    age: int = Field(default=None, gt=0)
    created_at : datetime | None = Field(default=datetime.now(timezone.utc))


class UsersOut(BaseModel):
    id: int 
    username: str = Field(max_length=100, min_length=3, unique=True, index=True)
    email: str = Field(max_length=100, min_length=10)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    age: int = Field(default=None, gt=0)
    created_at : datetime | None = Field(default=datetime.now(timezone.utc))


class Login(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    access_token: str
    token_type: str