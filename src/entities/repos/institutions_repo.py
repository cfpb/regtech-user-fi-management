from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from entities.models import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    FinancialInstitutionDto,
    FinancialInsitutionDomainCreate,
    DeniedDomainDao,
)


async def get_institutions(
    session: AsyncSession,
    leis: List[str] = None,
    domain: str = "",
    page: int = 0,
    count: int = 100,
) -> List[FinancialInstitutionDao]:
    async with session.begin():
        stmt = (
            select(FinancialInstitutionDao)
            .options(joinedload(FinancialInstitutionDao.domains))
            .limit(count)
            .offset(page * count)
        )
        if leis is not None:
            stmt = stmt.filter(FinancialInstitutionDao.lei.in_(leis))
        elif d := domain.strip():
            stmt = stmt.join(FinancialInstitutionDomainDao).filter(FinancialInstitutionDomainDao.domain == d)
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


async def upsert_institution(session: AsyncSession, fi: FinancialInstitutionDto) -> FinancialInstitutionDao:
    async with session.begin():
        stmt = select(FinancialInstitutionDao).filter(FinancialInstitutionDao.lei == fi.lei)
        res = await session.execute(stmt)
        db_fi = res.scalar_one_or_none()
        fi_data = fi.__dict__.copy()
        fi_data.pop("_sa_instance_state", None)
        if db_fi is None:
            db_fi = FinancialInstitutionDao(**fi_data)
            session.add(db_fi)
        else:
            for key, value in fi_data.items():
                setattr(db_fi, key, value)
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


async def is_domain_allowed(session: AsyncSession, domain: str) -> bool:
    if domain:
        async with session:
            stmt = select(func.count()).filter(DeniedDomainDao.domain == domain)
            res = await session.scalar(stmt)
            return res == 0
    return False
