from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['sha512_crypt'], deprecated='auto')


class Hasher:
    @staticmethod
    async def get_psw_hash(psw: str) -> str:
        return pwd_context.hash(secret=psw)

    @staticmethod
    async def verify_psw(psw_to_check: str, hashed_psw: str) -> bool:
        return pwd_context.verify(secret=psw_to_check, hash=hashed_psw)
