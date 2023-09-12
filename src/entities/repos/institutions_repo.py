from typing import List

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from entities.models import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    FinancialInstitutionDto,
    FinancialInsitutionDomainCreate,
)


async def get_institutions(
    session: AsyncSession, domain: str = "", page: int = 0, count: int = 100, leis: List[str] = []
) -> List[FinancialInstitutionDao]:
    async with session.begin():
        stmt = (
            select(FinancialInstitutionDao)
            .options(joinedload(FinancialInstitutionDao.domains))
            .limit(count)
            .offset(page * count)
        )
        if leis:
            stmt = stmt.filter(FinancialInstitutionDao.lei.in_(leis))
        elif d := domain.strip():
            search = "%{}%".format(d)
            stmt = stmt.join(
                FinancialInstitutionDomainDao,
                FinancialInstitutionDao.lei == FinancialInstitutionDomainDao.lei,
            ).filter(FinancialInstitutionDomainDao.domain.like(search))
        res = await session.scalars(stmt)
        return res.unique().all()


async def get_institution(session: AsyncSession, lei: str) -> FinancialInstitutionDao:
    async with session.begin():
        stmt = (
            select(FinancialInstitutionDao)
            .options(joinedload(FinancialInstitutionDao.domains))
            .filter(FinancialInstitutionDao.lei == lei)
        )
        return await session.scalar(stmt)


async def upsert_institution(
    session: AsyncSession, fi: FinancialInstitutionDto
) -> FinancialInstitutionDao:
    async with session.begin():
        stmt = select(FinancialInstitutionDao).filter(
            FinancialInstitutionDao.lei == fi.lei
        )
        res = await session.execute(stmt)
        db_fi = res.scalar_one_or_none()
        if db_fi is None:
            db_fi = FinancialInstitutionDao(lei=fi.lei, name=fi.name)
            session.add(db_fi)
        else:
            db_fi.name = fi.name
        await session.commit()
        return db_fi


async def add_domains(
    session: AsyncSession, lei: str, domains: List[FinancialInsitutionDomainCreate]
) -> List[FinancialInstitutionDomainDao]:
    async with session.begin():
        daos = set(
            map(
                lambda dto: FinancialInstitutionDomainDao(domain=dto.domain, lei=lei),
                domains,
            )
        )
        session.add_all(daos)
        await session.commit()
        return daos
