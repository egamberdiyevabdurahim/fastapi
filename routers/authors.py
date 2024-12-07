from schemas.authors import AuthorsIn, AuthorsOut

from urllib import request

from sqlalchemy.orm import Session

from sqlmodel import select

from fastapi import HTTPException, Depends, APIRouter

from core.models import Authors
from core.databases import SessionDep

router = APIRouter(    
    tags=['Authors'],
 )


@router.post("/author/", status_code=201, response_model=AuthorsOut)
async def create_author(author: AuthorsIn, session: Session = Depends(SessionDep)):
 
    author_in = AuthorsIn(**author.dic())
    session.add(author_in)
    session.commit()
    session.refresh(author_in)
    return author_in


@router.get("/authors/",  status_code=200, response_model=list[AuthorsOut])
async def list_authors(session: Session = Depends(SessionDep)):
    authors = session.exec(select(Authors)).all()
    return authors


@router.get("/author/{author_id}", status_code=200, response_model=AuthorsOut)
async def get_author(session: Session = Depends(SessionDep)):
    authors = session.exec(select(Authors)).all()
    return authors


@router.put("/update-authors/{author_id}" , status_code=200, response_model=AuthorsOut)
async def update_author(author_id: int, session: Session = Depends(SessionDep)):
    author = session.execute(select(Authors).where(Authors.id == author_id)).scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    data = await request.json()

    for key, value in data.items():
        if hasattr(author, key):
            setattr(author, key, value)

    session.commit()
    session.refresh(author)

    return {"status": True,
             "detail": "Updated successfully", "data": {
        "id": author.id,
        "first_name": author.first_name,
        "last_name": author.last_name,
        "age": author.age
    }}


@router.delete("/delete-author/{author_id}")
async def delete_author(author_id: int, session: Session = Depends(SessionDep)):
    authors = session.exec(select(Authors)).where(Authors.id == author_id).first()
    if not authors:
        raise HTTPException(status_code=404, detail="Author not found")

    session.delete(authors)
    session.commit()
    return {'status': True, 'detail': 'Deleted successfully'}