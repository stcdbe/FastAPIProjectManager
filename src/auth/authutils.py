from datetime import timedelta, datetime

import bcrypt
from jwt import encode

from src.config import settings


async def generate_token(user_id: str, expires_delta: timedelta) -> str:
    expires = datetime.utcnow() + expires_delta
    to_encode = {'exp': expires, 'sub': user_id}
    encoded_jwt = encode(payload=to_encode,
                         key=settings.JWT_SECRET_KEY,
                         algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


class Hasher:
    @staticmethod
    def get_psw_hash(psw: str) -> str:
        return (bcrypt.hashpw(password=psw.encode(), salt=bcrypt.gensalt())).decode()

    @staticmethod
    def verify_psw(psw_to_check: str, hashed_psw: str) -> bool:
        return bcrypt.checkpw(password=psw_to_check.encode(), hashed_password=hashed_psw.encode())
