from src.modules.user.entities.user import UserCreateData, UserPatchData
from src.modules.user.views.user.schemas import UserCreateScheme, UserPatchScheme


def convert_user_create_data_scheme_to_entity(scheme: UserCreateScheme) -> UserCreateData:
    return UserCreateData(
        username=scheme.username,
        email=scheme.email,
        password=scheme.password,
        first_name=scheme.first_name,
        second_name=scheme.second_name,
        gender=scheme.gender,
        company=scheme.company,
        join_date=scheme.join_date,
        job_title=scheme.job_title,
        date_of_birth=scheme.date_of_birth,
    )


def convert_user_patch_data_scheme_to_entity(scheme: UserPatchScheme) -> UserPatchData:
    return UserPatchData(
        username=scheme.username,
        email=scheme.email,
        password=scheme.password,
        first_name=scheme.first_name,
        second_name=scheme.second_name,
        gender=scheme.gender,
        company=scheme.company,
        join_date=scheme.join_date,
        job_title=scheme.job_title,
        date_of_birth=scheme.date_of_birth,
    )
