import os
from http import HTTPStatus
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from entities.engine import get_session
from entities.repos import institutions_repo as repo


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
    open_endpoints = os.getenv(
        "OPEN_ENDPOINT_PATHS",
        "/v1/admin/me,/v1/institutions,/v1/institutions/domains/allowed",
    )
    open_methods = os.getenv("OPEN_ENDPOINT_METHODS", "GET")
    endpoints = open_endpoints.split(",")
    methods = open_methods.split(",")
    return not (
        request.scope["path"].rstrip("/") in endpoints
        and request.scope["method"] in methods
    )


async def email_domain_denied(session: AsyncSession, email: str) -> bool:
    return not await repo.is_email_domain_allowed(session, email)
