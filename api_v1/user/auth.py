import bcrypt


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
