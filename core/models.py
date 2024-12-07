from datetime import datetime, timezone

from core.databases import engine

from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(max_length=100, min_length=3, unique=True, index=True)
    password : str = Field(max_length=50, min_length=8)
    email: str = Field(max_length=100, min_length=10)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    age: int = Field(default=None, gt=0)
    is_active: bool = Field(default=False)
    created_at : datetime | None = Field(default=datetime.now(timezone.utc))


class Authors(SQLModel, table=True):
    id: int = Field(primary_key=True)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None,max_length=100)
    age: int = Field(default=None, gt=0)


class Books(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field(max_length=100, nullable=False)
    author_id: int = Field(foreign_key="authors.id", nullable=False)


def create_tables():
    SQLModel.metadata.create_all(engine)