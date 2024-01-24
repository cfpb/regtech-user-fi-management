from fastapi import Depends, Request, HTTPException
from http import HTTPStatus
from regtech_api_commons.oauth2.oauth2_admin import OAuth2Admin
from regtech_api_commons.api import Router
from dependencies import check_domain, parse_leis, get_email_domain
from typing import Annotated, List, Tuple, Literal
from entities.engine import get_session
from entities.repos import institutions_repo as repo
from entities.models import (
    FinancialInstitutionDto,
    FinancialInstitutionWithRelationsDto,
    FinancialInsitutionDomainDto,
    FinancialInsitutionDomainCreate,
    FinanicialInstitutionAssociationDto,
    InstitutionTypeDto,
    AddressStateDto,
    FederalRegulatorDto,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.authentication import requires
from regtech_api_commons.models.auth import AuthenticatedUser

InstitutionType = Literal["sbl", "hmda"]


async def set_db(request: Request, session: Annotated[AsyncSession, Depends(get_session)]):
    request.state.db_session = session


router = Router(dependencies=[Depends(set_db)])


@router.get("/", response_model=List[FinancialInstitutionWithRelationsDto])
@requires("authenticated")
async def get_institutions(
    request: Request,
    leis: List[str] = Depends(parse_leis),
    domain: str = "",
    page: int = 0,
    count: int = 100,
):
    return await repo.get_institutions(request.state.db_session, leis, domain, page, count)


@router.post("/", response_model=Tuple[str, FinancialInstitutionWithRelationsDto], dependencies=[Depends(check_domain)])
@requires(["query-groups", "manage-users"])
async def create_institution(
    request: Request,
    fi: FinancialInstitutionDto,
):
    db_fi = await repo.upsert_institution(request.state.db_session, fi)
    kc_id = OAuth2Admin.upsert_group(fi.lei, fi.name)
    return kc_id, db_fi


@router.get("/associated", response_model=List[FinanicialInstitutionAssociationDto])
@requires("authenticated")
async def get_associated_institutions(request: Request):
    user: AuthenticatedUser = request.user
    email_domain = get_email_domain(user.email)
    associated_institutions = await repo.get_institutions(request.state.db_session, user.institutions)
    return [
        FinanicialInstitutionAssociationDto(
            **institution.__dict__,
            approved=email_domain in [inst_domain.domain for inst_domain in institution.domains],
        )
        for institution in associated_institutions
    ]


@router.get("/types/{type}", response_model=List[InstitutionTypeDto])
@requires("authenticated")
async def get_institution_types(request: Request, type: InstitutionType):
    match type:
        case "sbl":
            return await repo.get_sbl_types(request.state.db_session)
        case "hmda":
            return await repo.get_hmda_types(request.state.db_session)


@router.get("/address-states", response_model=List[AddressStateDto])
@requires("authenticated")
async def get_address_states(request: Request):
    return await repo.get_address_states(request.state.db_session)


@router.get("/regulators", response_model=List[FederalRegulatorDto])
@requires("authenticated")
async def get_federal_regulators(request: Request):
    return await repo.get_federal_regulators(request.state.db_session)


@router.get("/{lei}", response_model=FinancialInstitutionWithRelationsDto)
@requires("authenticated")
async def get_institution(
    request: Request,
    lei: str,
):
    res = await repo.get_institution(request.state.db_session, lei)
    if not res:
        raise HTTPException(HTTPStatus.NOT_FOUND, f"{lei} not found.")
    return res


@router.post("/{lei}/domains/", response_model=List[FinancialInsitutionDomainDto], dependencies=[Depends(check_domain)])
@requires(["query-groups", "manage-users"])
async def add_domains(
    request: Request,
    lei: str,
    domains: List[FinancialInsitutionDomainCreate],
):
    return await repo.add_domains(request.state.db_session, lei, domains)


@router.get("/domains/allowed", response_model=bool)
async def is_domain_allowed(request: Request, domain: str):
    return await repo.is_domain_allowed(request.state.db_session, domain)
