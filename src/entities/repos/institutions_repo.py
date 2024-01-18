from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from .repo_utils import query_type

from entities.models import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    FinancialInstitutionDto,
    FinancialInsitutionDomainCreate,
    HMDAInstitutionTypeDao,
    SBLInstitutionTypeDao,
    DeniedDomainDao,
    AddressStateDao,
    FederalRegulatorDao,
    SblTypeMappingDao,
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


async def get_sbl_types(session: AsyncSession) -> List[SBLInstitutionTypeDao]:
    return await query_type(session, SBLInstitutionTypeDao)


async def get_hmda_types(session: AsyncSession) -> List[HMDAInstitutionTypeDao]:
    return await query_type(session, HMDAInstitutionTypeDao)


async def get_address_states(session: AsyncSession) -> List[AddressStateDao]:
    return await query_type(session, AddressStateDao)


async def get_federal_regulators(session: AsyncSession) -> List[FederalRegulatorDao]:
    return await query_type(session, FederalRegulatorDao)


async def upsert_institution(session: AsyncSession, fi: FinancialInstitutionDto) -> FinancialInstitutionDao:
    async with session.begin():
        fi_data = fi.__dict__.copy()
        fi_data.pop("_sa_instance_state", None)

        if "sbl_institution_types" in fi_data:
            types_association = [
                SblTypeMappingDao(type_id=t)
                if isinstance(t, str)
                else SblTypeMappingDao(type_id=t.id, details=t.details)
                for t in fi.sbl_institution_types
            ]
            fi_data["sbl_institution_types"] = types_association

        db_fi = await session.merge(FinancialInstitutionDao(**fi_data))
        await session.flush()
        await session.refresh(db_fi)
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
