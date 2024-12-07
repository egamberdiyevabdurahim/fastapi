from pydantic import BaseModel, Field


class AuthorsIn(BaseModel):
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None,max_length=100)
    age: int = Field(default=None, gt=0)


class AuthorsOut(BaseModel):
    id: int 
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None,max_length=100)
    age: int = Field(default=None, gt=0)