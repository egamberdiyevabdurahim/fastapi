from schemas.books import BooksIn, BooksOut

from fastapi import HTTPException, APIRouter, Depends, Request

from core.models import Books, Authors
from core.databases import get_session

from sqlalchemy.orm import Session

from sqlmodel import select


router = APIRouter(
        tags=['Books'],
)


@router.post("/book/", status_code=201, response_model=BooksOut)
async def create_book(book: BooksIn, session: Session = Depends(get_session)):
    author = session.execute(select(Authors).where(Authors.id == book.author_id)).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_book = Books(**book.dict())
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book


@router.get("/books/", status_code=200, response_model=list[BooksOut])
async def list_books(session: Session = Depends(get_session)):
    books = session.exec(select(Books)).all()
    return books


@router.get("/book/{book_id}", status_code=200, response_model=BooksOut)
async def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.execute(select(Books).where(Books.id == book_id)).scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/book/{book_id}", status_code=200, response_model=BooksOut)
async def update_book(book_id: int, request: Request, session: Session = Depends(get_session)):
    book = session.execute(select(Books).where(Books.id == book_id)).scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    data = await request.json()
    for key, value in data.items():
        if hasattr(book, key):
            setattr(book, key, value)

    session.commit()
    session.refresh(book)
    return book


@router.delete("/delete-book/{book_id}", status_code=204)
async def delete_book(book_id: int, session: Session = Depends(get_session)):
    books = session.exec(select(Books)).where(Books.id == book_id).first()
    if not books:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(books)
    session.commit()
    return {'status': True, 'detail': 'Deleted successfully'}