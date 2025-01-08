from typing import List, Sequence, Set

from sqlalchemy.orm import Session

from regtech_api_commons.models.auth import AuthenticatedUser

from .repo_utils import get_associated_sbl_types

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


def get_institutions(
    session: Session,
    leis: List[str] | None = None,
    domain: str = "",
    page: int = 0,
    count: int = 100,
) -> Sequence[FinancialInstitutionDao]:
    query = session.query(FinancialInstitutionDao)
    if leis is not None:
        query = query.filter(FinancialInstitutionDao.lei.in_(leis))
    elif d := domain.strip():
        query = query.join(FinancialInstitutionDomainDao).filter(FinancialInstitutionDomainDao.domain == d)
    return query.limit(count).offset(page * count).all()


def get_institution(session: Session, lei: str) -> FinancialInstitutionDao | None:
    return session.get(FinancialInstitutionDao, lei)


def get_sbl_types(session: Session) -> Sequence[SBLInstitutionTypeDao]:
    return session.query(SBLInstitutionTypeDao).all()


def get_hmda_types(session: Session) -> Sequence[HMDAInstitutionTypeDao]:
    return session.query(HMDAInstitutionTypeDao).all()


def get_address_states(session: Session) -> Sequence[AddressStateDao]:
    return session.query(AddressStateDao).all()


def get_federal_regulators(session: Session) -> Sequence[FederalRegulatorDao]:
    return session.query(FederalRegulatorDao).all()


def upsert_institution(
    session: Session, fi: FinancialInstitutionDto, user: AuthenticatedUser
) -> FinancialInstitutionDao:
    fi_data = fi.__dict__.copy()
    fi_data.pop("_sa_instance_state", None)
    fi_data.pop("version", None)

    if "sbl_institution_types" in fi_data:
        types_association = get_associated_sbl_types(fi.lei, user.id, fi.sbl_institution_types)
        fi_data["sbl_institution_types"] = types_association

    db_fi = session.merge(FinancialInstitutionDao(**fi_data, modified_by=user.id))
    session.commit()
    return db_fi


def update_sbl_types(
    session: Session, user: AuthenticatedUser, lei: str, sbl_types: Sequence[SblTypeAssociationDto | str]
) -> FinancialInstitutionDao | None:
    if fi := get_institution(session, lei):
        new_types = set(get_associated_sbl_types(lei, user.id, sbl_types))
        old_types = set(fi.sbl_institution_types)
        add_types = new_types.difference(old_types)
        remove_types = old_types.difference(new_types)

        fi.sbl_institution_types = [type for type in fi.sbl_institution_types if type not in remove_types]
        fi.sbl_institution_types.extend(add_types)
        for type in fi.sbl_institution_types:
            type.version = fi.version
        session.commit()
        return fi


def add_domains(
    session: Session, lei: str, domains: List[FinancialInsitutionDomainCreate]
) -> Set[FinancialInstitutionDomainDao]:
    daos = set(
        map(
            lambda dto: FinancialInstitutionDomainDao(domain=dto.domain, lei=lei),
            domains,
        )
    )
    session.add_all(daos)
    session.commit()
    return daos


def is_domain_allowed(session: Session, domain: str) -> bool:
    if domain:
        return session.get(DeniedDomainDao, domain) is None
    return False
