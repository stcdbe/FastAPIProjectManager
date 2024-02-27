import bcrypt


class Hasher:
    @staticmethod
    def get_psw_hash(psw: str) -> str:
        return (bcrypt.hashpw(password=psw.encode(), salt=bcrypt.gensalt())).decode()

    @staticmethod
    def verify_psw(psw_to_check: str, hashed_psw: str) -> bool:
        return bcrypt.checkpw(password=psw_to_check.encode(), hashed_password=hashed_psw.encode())
