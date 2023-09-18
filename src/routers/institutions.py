from fastapi import Depends, Request, HTTPException
from http import HTTPStatus
from oauth2 import oauth2_admin
from util import Router
from dependencies import parse_leis
from typing import Annotated, List, Tuple
from entities.engine import get_session
from entities.repos import institutions_repo as repo
from entities.models import (
    FinancialInstitutionDto,
    FinancialInstitutionWithDomainsDto,
    FinancialInsitutionDomainDto,
    FinancialInsitutionDomainCreate,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.authentication import requires


async def set_db(request: Request, session: Annotated[AsyncSession, Depends(get_session)]):
    request.state.db_session = session


router = Router(dependencies=[Depends(set_db)])


@router.get("/", response_model=List[FinancialInstitutionWithDomainsDto])
@requires("authenticated")
async def get_institutions(
    request: Request,
    leis: List[str] = Depends(parse_leis),
    domain: str = "",
    page: int = 0,
    count: int = 100,
):
    return await repo.get_institutions(request.state.db_session, leis, domain, page, count)


@router.post("/", response_model=Tuple[str, FinancialInstitutionDto])
@requires(["query-groups", "manage-users"])
async def create_institution(
    request: Request,
    fi: FinancialInstitutionDto,
):
    db_fi = await repo.upsert_institution(request.state.db_session, fi)
    kc_id = oauth2_admin.upsert_group(fi.lei, fi.name)
    return kc_id, db_fi


@router.get("/{lei}", response_model=FinancialInstitutionWithDomainsDto)
@requires("authenticated")
async def get_institution(
    request: Request,
    lei: str,
):
    res = await repo.get_institution(request.state.db_session, lei)
    if not res:
        raise HTTPException(HTTPStatus.NOT_FOUND, f"{lei} not found.")
    return res


@router.post("/{lei}/domains/", response_model=List[FinancialInsitutionDomainDto])
@requires(["query-groups", "manage-users"])
async def add_domains(
    request: Request,
    lei: str,
    domains: List[FinancialInsitutionDomainCreate],
):
    return await repo.add_domains(request.state.db_session, lei, domains)


@router.get("/domains/allowed", response_model=bool)
async def is_domain_allowed(request: Request, domain: str):
    return await repo.is_email_domain_allowed(request.state.db_session, domain)
