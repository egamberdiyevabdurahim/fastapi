from schemas.users import UsersIn

from fastapi import HTTPException, APIRouter, Depends

from urllib import request

from core.models import Users
from core.databases import SessionDep

from sqlalchemy.orm import Session

from sqlmodel import select


router = APIRouter(
        tags=['Users'],
)

@router.post("/user/", response_model=dict)
async def create_user(user: UsersIn, session: Session = Depends(SessionDep)):
 
    user_in = UsersIn(**user.dic())
    session.add(user_in)
    session.commit()
    session.refresh(user_in)
    return user_in

@router.get("/users/")
async def list_users(session: Session = Depends(SessionDep)):
    users = session.exec(select(Users)).all()
    return users


@router.get("/user/{user_id}")
async def get_user(session: Session = Depends(SessionDep)):
    users = session.exec(select(Users)).all()
    return users


@router.put("/update-user/{user_id}" ,status_code=200)
async def update_user(user_id: int, session: Session = Depends(SessionDep)):
    user = session.execute(select(Users).where(Users.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    data = await request.json()

    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    session.commit()
    session.refresh(user)

    return {"status": True,
             "detail": "Updated successfully", "data": {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "age": user.age
    }}


@router.delete("/delete-user/{user_id}")
async def delete_user(user_id: int, session: Session = Depends(SessionDep)):
    users = session.exec(select(Users)).where(Users.id == user_id).first()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(users)
    session.commit()
    return {'status': True, 'detail': 'Deleted successfully'}