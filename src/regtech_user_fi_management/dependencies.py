from http import HTTPStatus
from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from regtech_user_fi_management.entities.engine.engine import get_session
import regtech_user_fi_management.entities.repos.institutions_repo as repo
from regtech_api_commons.api.exceptions import RegTechHttpException
from regtech_api_commons.api.dependencies import get_email_domain


async def check_domain(request: Request, session: Annotated[AsyncSession, Depends(get_session)]) -> None:
    if not request.user.is_authenticated:
        raise RegTechHttpException(
            status_code=HTTPStatus.FORBIDDEN, name="Request Forbidden", detail="unauthenticated user"
        )
    if await email_domain_denied(session, get_email_domain(request.user.email)):
        raise RegTechHttpException(
            status_code=HTTPStatus.FORBIDDEN, name="Request Forbidden", detail="email domain denied"
        )


async def email_domain_denied(session: AsyncSession, email: str) -> bool:
    return not await repo.is_domain_allowed(session, email)
