from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_session

SQLAlchemySessionDep = Annotated[AsyncSession, Depends(get_session)]
