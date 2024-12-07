from core.security.auth import get_password_hash, get_user_by_username, get_user_by_email, validate_password, verify_password
from core.security.jwt_token import create_token
from core.models import Users
from core.databases import SessionDep

from schemas.users import Login, TokenData, UsersIn, UsersOut

from fastapi import HTTPException, APIRouter, status


router = APIRouter()


@router.post("/register/", status_code=status.HTTP_200_OK)
async def register(user_in: UsersIn, session: SessionDep) -> UsersOut:
    error_message = None
    if not validate_password(password=user_in.password, confirm_password=user_in.confirm_password):
        error_message = "Password does not match"
    elif get_user_by_username(user_in.username, session=session):
        error_message = "Username already exists"
    elif get_user_by_email(user_in.email, session=session):
        error_message = "Email already exists"

    if error_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message 
        )

    user_dict = dict(user_in)
    user_dict.pop('confirm_password')
    user_dict['password'] = get_password_hash(user_in.password)

    user = Users(**user_dict)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login/")
async def login(data: Login, session: SessionDep) -> TokenData:
    user = get_user_by_username(username=data.username, session=session)
    if not user or not verify_password(plain_password=data.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is incorrect"
        )
    access_token = create_token(data={"sub": user.username}, exipre_delta=None)
    return TokenData(access_token=access_token, token_type="bearer")


@router.post("/logout/")
async def logout():
    pass


@router.post("/verify-code/")
async def verify_code():
    pass


@router.post("/resend-code/")
async def resend_code():
    pass