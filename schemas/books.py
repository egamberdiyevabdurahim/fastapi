from pydantic import BaseModel, Field


class BooksIn(BaseModel):
    id: int = Field(primary_key=True)
    title: str = Field(max_length=100, nullable=False)
    author: int = Field(foreign_key="authors.firs_name", nullable=False)


class BooksOut(BaseModel):
    id: int = Field(primary_key=True)
    title: str = Field(max_length=100, nullable=False)
    author: int = Field(foreign_key="authors.firs_name", nullable=False)