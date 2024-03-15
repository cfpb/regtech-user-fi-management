import functools

from http import HTTPStatus
from typing import Annotated
from fastapi import Depends, Query, HTTPException, Request, Response
from fastapi.types import DecoratedCallable
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from itertools import chain

from entities.engine import get_session
from entities.repos import institutions_repo as repo
from starlette.authentication import AuthCredentials
from regtech_api_commons.models.auth import AuthenticatedUser


async def check_domain(request: Request, session: Annotated[AsyncSession, Depends(get_session)]) -> None:
    if not request.user.is_authenticated:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
    if await email_domain_denied(session, get_email_domain(request.user.email)):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="email domain denied")


async def email_domain_denied(session: AsyncSession, email: str) -> bool:
    return not await repo.is_domain_allowed(session, email)


def parse_leis(leis: List[str] = Query(None)) -> Optional[List]:
    """
    Parses leis from list of one or multiple strings to a list of
    multiple distinct lei strings.
    Returns empty list when nothing is passed in
    Ex1: ['lei1,lei2'] -> ['lei1', 'lei2']
    Ex2: ['lei1,lei2', 'lei3,lei4'] -> ['lei1','lei2','lei3','lei4']
    """

    if leis:
        return list(chain.from_iterable([x.split(",") for x in leis]))
    else:
        return None


def get_email_domain(email: str) -> str:
    if email:
        return email.split("@")[-1]
    return None


admin_scopes = set(["query-groups", "manage-users"])


def is_admin(auth: AuthCredentials):
    return admin_scopes.issubset(auth.scopes)


def lei_association_check(func: DecoratedCallable) -> DecoratedCallable:
    @functools.wraps(func)
    async def wrapper(request: Request, *args, **kwargs) -> Response:
        lei = kwargs.get("lei")
        user: AuthenticatedUser = request.user
        auth: AuthCredentials = request.auth
        if not is_admin(auth) and lei not in user.institutions:
            raise HTTPException(HTTPStatus.FORBIDDEN, detail=f"LEI {lei} is not associated with the user.")
        return await func(request, *args, **kwargs)

    return wrapper  # type: ignore[return-value]


def fi_search_association_check(func: DecoratedCallable) -> DecoratedCallable:
    def verify_leis(user: AuthenticatedUser, leis: List[str]) -> None:
        if not set(filter(len, leis)).issubset(set(filter(len, user.institutions))):
            raise HTTPException(
                HTTPStatus.FORBIDDEN,
                detail=f"Institutions query with LEIs ({leis}) not associated with user is forbidden.",
            )

    def verify_domain(user: AuthenticatedUser, domain: str) -> None:
        if domain != get_email_domain(user.email):
            raise HTTPException(
                HTTPStatus.FORBIDDEN,
                detail=f"Institutions query with domain ({domain}) not associated with user is forbidden.",
            )

    @functools.wraps(func)
    async def wrapper(request: Request, *args, **kwargs) -> Response:
        user: AuthenticatedUser = request.user
        auth: AuthCredentials = request.auth
        if not is_admin(auth):
            leis = kwargs.get("leis")
            domain = kwargs.get("domain")
            if leis:
                verify_leis(user, leis)
            elif domain:
                verify_domain(user, domain)
            elif not leis and not domain:
                raise HTTPException(HTTPStatus.FORBIDDEN, detail="Retrieving institutions without filter is forbidden.")
        return await func(request=request, *args, **kwargs)

    return wrapper  # type: ignore[return-value]
