from fastapi import Depends, Request, Response
from http import HTTPStatus
from regtech_api_commons.oauth2.oauth2_admin import OAuth2Admin
from regtech_user_fi_management.config import kc_settings
from regtech_api_commons.api.router_wrapper import Router
from regtech_user_fi_management.dependencies import (
    check_domain,
)
from typing import Annotated, List, Tuple, Literal
from regtech_user_fi_management.entities.engine.engine import get_session
import regtech_user_fi_management.entities.repos.institutions_repo as repo
from regtech_user_fi_management.entities.models.dto import (
    FinancialInstitutionDto,
    FinancialInstitutionWithRelationsDto,
    FinancialInsitutionDomainDto,
    FinancialInsitutionDomainCreate,
    FinancialInstitutionAssociationDto,
    InstitutionTypeDto,
    AddressStateDto,
    FederalRegulatorDto,
    SblTypeAssociationDetailsDto,
    SblTypeAssociationPatchDto,
    VersionedData,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.authentication import requires
from regtech_api_commons.models.auth import AuthenticatedUser
from regtech_api_commons.api.exceptions import RegTechHttpException
from regtech_api_commons.api.dependencies import (
    verify_institution_search,
    verify_user_lei_relation,
    parse_leis,
    get_email_domain,
)

oauth2_admin = OAuth2Admin(kc_settings)

InstitutionType = Literal["sbl", "hmda"]


async def set_db(request: Request, session: Annotated[AsyncSession, Depends(get_session)]):
    request.state.db_session = session


router = Router(dependencies=[Depends(set_db)])


@router.get(
    "/", response_model=List[FinancialInstitutionWithRelationsDto], dependencies=[Depends(verify_institution_search)]
)
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
    db_fi = await repo.upsert_institution(request.state.db_session, fi, request.user)
    kc_id = oauth2_admin.upsert_group(fi.lei, fi.name)
    return kc_id, db_fi


@router.get("/associated", response_model=List[FinancialInstitutionAssociationDto])
@requires("authenticated")
async def get_associated_institutions(request: Request):
    user: AuthenticatedUser = request.user
    email_domain = get_email_domain(user.email)
    associated_institutions = await repo.get_institutions(request.state.db_session, user.institutions)
    return [
        FinancialInstitutionAssociationDto(
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


@router.get(
    "/{lei}", response_model=FinancialInstitutionWithRelationsDto, dependencies=[Depends(verify_user_lei_relation)]
)
@requires("authenticated")
async def get_institution(
    request: Request,
    lei: str,
):
    res = await repo.get_institution(request.state.db_session, lei)
    if not res:
        raise RegTechHttpException(HTTPStatus.NOT_FOUND, name="Institution Not Found", detail=f"{lei} not found.")
    return res


@router.get(
    "/{lei}/types/{type}",
    response_model=VersionedData[List[SblTypeAssociationDetailsDto]] | None,
    dependencies=[Depends(verify_user_lei_relation)],
)
@requires("authenticated")
async def get_types(request: Request, response: Response, lei: str, type: InstitutionType):
    match type:
        case "sbl":
            if fi := await repo.get_institution(request.state.db_session, lei):
                return VersionedData(version=fi.version, data=fi.sbl_institution_types)
            else:
                response.status_code = HTTPStatus.NO_CONTENT
        case "hmda":
            raise RegTechHttpException(
                status_code=HTTPStatus.NOT_IMPLEMENTED, name="Not Supported", detail="HMDA type not yet supported"
            )


@router.put(
    "/{lei}/types/{type}",
    response_model=VersionedData[List[SblTypeAssociationDetailsDto]] | None,
    dependencies=[Depends(verify_user_lei_relation)],
)
@requires("authenticated")
async def update_types(
    request: Request, response: Response, lei: str, type: InstitutionType, types_patch: SblTypeAssociationPatchDto
):
    match type:
        case "sbl":
            if fi := await repo.update_sbl_types(
                request.state.db_session, request.user, lei, types_patch.sbl_institution_types
            ):
                return VersionedData(version=fi.version, data=fi.sbl_institution_types)
            else:
                response.status_code = HTTPStatus.NO_CONTENT
        case "hmda":
            raise RegTechHttpException(
                status_code=HTTPStatus.NOT_IMPLEMENTED, name="Not Supported", detail="HMDA type not yet supported"
            )


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
