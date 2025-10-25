from src.data.models.user.user_model import UserModel
from src.domain.user.entities import User
from src.domain.user.enums import UserGender


def convert_user_model_to_entity(user_model: UserModel) -> User:
    if user_model.gender is None:
        gender = None
    else:
        gender = UserGender(user_model.gender)

    return User(
        guid=user_model.guid,
        username=user_model.username,
        email=user_model.email,
        password=user_model.password,
        first_name=user_model.first_name,
        second_name=user_model.second_name,
        gender=gender,
        company=user_model.company,
        join_date=user_model.join_date,
        job_title=user_model.job_title,
        date_of_birth=user_model.date_of_birth,
        created_at=user_model.created_at,
        updated_at=user_model.updated_at,
        is_deleted=user_model.is_deleted,
        deleted_at=user_model.deleted_at,
    )
