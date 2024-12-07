from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from core.models import create_tables

from routers import users, books, authors, auth


app = FastAPI()


@app.on_event("startup")
async def startup():
    create_tables()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(authors.router)
app.include_router(books.router)


@app.get('/', tags=["root"])
async def root():
    return RedirectResponse(url="/docs")