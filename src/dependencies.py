from http import HTTPStatus
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from entities.engine import get_session
from entities.repos import institutions_repo as repo

OPEN_DOMAIN_REQUESTS = {
    "/v1/admin/me": {"GET"},
    "/v1/institutions": {"GET"},
    "/v1/institutions/domains/allowed": {"GET"},
}


async def check_domain(
    request: Request, session: Annotated[AsyncSession, Depends(get_session)]
) -> None:
    if request_needs_domain_check(request):
        if not request.user.is_authenticated:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
        if await email_domain_denied(session, request.user.email):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="email domain denied"
            )


def request_needs_domain_check(request: Request) -> bool:
    path = request.scope["path"].rstrip("/")
    return not (
        path in OPEN_DOMAIN_REQUESTS
        and request.scope["method"] in OPEN_DOMAIN_REQUESTS[path]
    )


async def email_domain_denied(session: AsyncSession, email: str) -> bool:
    return not await repo.is_email_domain_allowed(session, email)
