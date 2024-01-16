from uuid import UUID

from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import DBAPIError
from asyncpg.exceptions import DataError

from src.database.dbmodels import ProjectDB, TaskDB
from src.project.projectschemas import ProjectCreate, TaskCreate, ProjectPatch, TaskPatch


async def get_project_db(session: AsyncSession, project_id: UUID) -> ProjectDB | None:
    stmt = select(ProjectDB).where(ProjectDB.id == project_id)
    try:
        return (await session.execute(stmt)).scalars().first()
    except (DBAPIError, DataError):
        await session.rollback()


async def get_project_with_tasks_db(session: AsyncSession, project_id: UUID) -> ProjectDB | None:
    stmt = (select(ProjectDB)
            .where(ProjectDB.id == project_id)
            .options(selectinload(ProjectDB.tasks)))
    try:
        return (await session.execute(stmt)).scalars().first()
    except (DBAPIError, DataError):
        await session.rollback()


async def get_some_projects_db(session: AsyncSession,
                               offset: int,
                               limit: int,
                               ordering: str,
                               reverse: bool = False) -> list[ProjectDB]:
    stmt = (select(ProjectDB)
            .offset(offset)
            .limit(limit))
    if reverse:
        stmt = stmt.order_by(desc(ordering))
    else:
        stmt = stmt.order_by(ordering)
    return list((await session.execute(stmt)).scalars().all())


async def create_project_db(session: AsyncSession,
                            project_data: ProjectCreate,
                            creator_id: UUID) -> ProjectDB:
    new_project = ProjectDB(creator_id=creator_id)

    for key, val in project_data.model_dump().items():
        setattr(new_project, key, val)

    session.add(new_project)
    await session.commit()
    return new_project


async def patch_project_db(session: AsyncSession,
                           project: ProjectDB,
                           upd_project_data: ProjectPatch) -> ProjectDB:
    for key, val in upd_project_data.model_dump(exclude_none=True, exclude_unset=True).items():
        setattr(project, key, val)

    await session.commit()
    await session.refresh(project)
    return project


async def del_project_db(session: AsyncSession, project: ProjectDB) -> None:
    try:
        await session.delete(project)
        await session.commit()
    except (UnmappedInstanceError, AttributeError):
        await session.rollback()


async def create_project_task_db(session: AsyncSession,
                                 project: ProjectDB,
                                 task_data: TaskCreate,
                                 executor_id: UUID) -> ProjectDB:
    new_task = TaskDB(project_id=project.id, executor_id=executor_id)

    for key, val in task_data.model_dump().items():
        setattr(new_task, key, val)

    project.tasks.append(new_task)
    await session.commit()
    await session.refresh(project)
    return project


async def patch_project_task_db(session: AsyncSession,
                                project: ProjectDB,
                                task_id: UUID,
                                upd_task_data: TaskPatch) -> ProjectDB:
    for task in project.tasks:
        if task.id == task_id:
            for key, val in upd_task_data.model_dump(exclude_none=True, exclude_unset=True).items():
                setattr(task, key, val)
            break
    await session.commit()
    await session.refresh(project)
    return project


async def del_project_task_db(session: AsyncSession,
                              project: ProjectDB,
                              task_id: UUID) -> None:
    for index, task in enumerate(project.tasks):
        if task.id == task_id:
            del project.tasks[index]
            break
    await session.commit()
