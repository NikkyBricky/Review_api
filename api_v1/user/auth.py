import bcrypt
from fastapi import HTTPException, status


def hash_password(password):
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password


def check_password(correct_hashed_password, password):
    result = bcrypt.checkpw(
        password=password.encode(),
        hashed_password=correct_hashed_password,
    )
    if result:
        return result
    #TODO Опять же привязаны к фастапи
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={"message": "password is incorrect"}
    )
