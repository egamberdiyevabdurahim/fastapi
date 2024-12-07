import jwt 

from datetime import timedelta, datetime

SECRET_KEY = "6b4b58f9c835be4b1b1219e7152c3c594c2c5e2dbb4b8a2439f8508a5e284f34"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

def create_token(data: dict, exipre_delta: timedelta | None):
    to_encode = data.copy()
    if exipre_delta:
        expire = datetime.utcnow() + exipre_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token