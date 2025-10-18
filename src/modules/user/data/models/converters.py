from src.modules.user.data.models.user_model import UserModel
from src.modules.user.entities.user import User


def convert_user_model_to_entity(user_model: UserModel) -> User:
    return User(
        guid: UUID,
        username: str,
        email: str,
        password: str,
        first_name: str | None,
        second_name: str | None,
        gender: UserGender | None,
        company: str | None,
        join_date: date | None,
        job_title: str | None,
        date_of_birth: date | None
    )
