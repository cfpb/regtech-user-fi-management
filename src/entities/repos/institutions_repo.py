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
        if db_fi is None:
            db_fi = FinancialInstitutionDao(
                lei=fi.lei,
                name=fi.name,
                tax_id=fi.tax_id,
                rssd_id=fi.rssd_id,
                primary_federal_regulator_id=fi.primary_federal_regulator_id,
                hmda_institution_type_id=fi.hmda_institution_type_id,
                sbl_institution_type_id=fi.sbl_institution_type_id,
                hq_address_street_1=fi.hq_address_street_1,
                hq_address_street_2=fi.hq_address_street_2,
                hq_address_city=fi.hq_address_city,
                hq_address_state_code=fi.hq_address_state_code,
                hq_address_zip=fi.hq_address_zip,
                parent_lei=fi.parent_lei,
                parent_legal_name=fi.parent_legal_name,
                parent_rssd_id=fi.parent_rssd_id,
                top_holder_lei=fi.top_holder_lei,
                top_holder_legal_name=fi.top_holder_legal_name,
                top_holder_rssd_id=fi.top_holder_rssd_id,
            )
            session.add(db_fi)
        else:
            db_fi.name = fi.name
            db_fi.tax_id = fi.tax_id
            db_fi.rssd_id = fi.rssd_id
            db_fi.primary_federal_regulator_id = fi.primary_federal_regulator_id
            db_fi.hmda_institution_type_id = fi.hmda_institution_type_id
            db_fi.sbl_institution_type_id = fi.sbl_institution_type_id
            db_fi.hq_address_street_1 = fi.hq_address_street_1
            db_fi.hq_address_street_2 = fi.hq_address_street_2
            db_fi.hq_address_city = fi.hq_address_city
            db_fi.hq_address_state_code = fi.hq_address_state_code
            db_fi.hq_address_zip = fi.hq_address_zip
            db_fi.parent_lei = fi.parent_lei
            db_fi.parent_legal_name = fi.parent_legal_name
            db_fi.parent_rssd_id = fi.parent_rssd_id
            db_fi.top_holder_lei = fi.top_holder_lei
            db_fi.top_holder_legal_name = fi.top_holder_legal_name
            db_fi.top_holder_rssd_id = fi.top_holder_rssd_id
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
