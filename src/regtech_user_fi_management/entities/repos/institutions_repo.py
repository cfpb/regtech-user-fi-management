from typing import List, Sequence, Set

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from regtech_api_commons.models.auth import AuthenticatedUser

from .repo_utils import get_associated_sbl_types, query_type

from regtech_user_fi_management.entities.models.dao import (
    FinancialInstitutionDao,
    FinancialInstitutionDomainDao,
    HMDAInstitutionTypeDao,
    SBLInstitutionTypeDao,
    DeniedDomainDao,
    AddressStateDao,
    FederalRegulatorDao,
)

from regtech_user_fi_management.entities.models.dto import (
    FinancialInstitutionDto,
    FinancialInsitutionDomainCreate,
    SblTypeAssociationDto,
)


async def get_institutions(
    session: AsyncSession,
    leis: List[str] | None = None,
    domain: str = "",
    page: int = 0,
    count: int = 100,
) -> Sequence[FinancialInstitutionDao]:
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


async def get_institution(session: AsyncSession, lei: str) -> FinancialInstitutionDao | None:
    async with session.begin():
        stmt = (
            select(FinancialInstitutionDao)
            .options(joinedload(FinancialInstitutionDao.domains))
            .filter(FinancialInstitutionDao.lei == lei)
        )
        return await session.scalar(stmt)


async def get_sbl_types(session: AsyncSession) -> Sequence[SBLInstitutionTypeDao]:
    return await query_type(session, SBLInstitutionTypeDao)


async def get_hmda_types(session: AsyncSession) -> Sequence[HMDAInstitutionTypeDao]:
    return await query_type(session, HMDAInstitutionTypeDao)


async def get_address_states(session: AsyncSession) -> Sequence[AddressStateDao]:
    return await query_type(session, AddressStateDao)


async def get_federal_regulators(session: AsyncSession) -> Sequence[FederalRegulatorDao]:
    return await query_type(session, FederalRegulatorDao)


async def upsert_institution(
    session: AsyncSession, fi: FinancialInstitutionDto, user: AuthenticatedUser
) -> FinancialInstitutionDao:
    async with session.begin():
        fi_data = fi.__dict__.copy()
        fi_data.pop("_sa_instance_state", None)
        fi_data.pop("version", None)

        if "sbl_institution_types" in fi_data:
            types_association = get_associated_sbl_types(fi.lei, user.id, fi.sbl_institution_types)
            fi_data["sbl_institution_types"] = types_association

        db_fi = await session.merge(FinancialInstitutionDao(**fi_data, modified_by=user.id))
        await session.flush()
        await session.refresh(db_fi)
        return db_fi


async def update_sbl_types(
    session: AsyncSession, user: AuthenticatedUser, lei: str, sbl_types: Sequence[SblTypeAssociationDto | str]
) -> FinancialInstitutionDao | None:
    if fi := await get_institution(session, lei):
        new_types = set(get_associated_sbl_types(lei, user.id, sbl_types))
        old_types = set(fi.sbl_institution_types)
        add_types = new_types.difference(old_types)
        remove_types = old_types.difference(new_types)

        fi.sbl_institution_types = [type for type in fi.sbl_institution_types if type not in remove_types]
        fi.sbl_institution_types.extend(add_types)
        for type in fi.sbl_institution_types:
            type.version = fi.version
        await session.commit()
        """
        load the async relational attributes so dto can be properly serialized
        """
        for type in fi.sbl_institution_types:
            await type.awaitable_attrs.sbl_type
        return fi


async def add_domains(
    session: AsyncSession, lei: str, domains: List[FinancialInsitutionDomainCreate]
) -> Set[FinancialInstitutionDomainDao]:
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
