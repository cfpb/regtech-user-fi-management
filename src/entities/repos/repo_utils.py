from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, TypeVar

T = TypeVar("T")


async def query_type(session: AsyncSession, type: T) -> List[T]:
    async with session.begin():
        stmt = select(type)
        res = await session.scalars(stmt)
        return res.all()
