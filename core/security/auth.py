from passlib.context import CryptContext

from core.databases import SessionDep
from core.models import Users

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)

def validate_password(password: str, confirm_password: str) -> bool:
    if password != confirm_password:
        return False
    return True


def get_user_by_username(username: str, session: SessionDep) -> None | Users:
    return session.query(Users).filter(Users.username == username).first()


def get_user_by_email(email: str, session: SessionDep) -> None | Users:
    return session.query(Users).filter(Users.email == email).first()