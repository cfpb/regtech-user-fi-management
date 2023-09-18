from http import HTTPStatus
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from itertools import chain

from fastapi import Query

from entities.engine import get_session
from entities.repos import institutions_repo as repo


async def check_domain(request: Request, session: Annotated[AsyncSession, Depends(get_session)]) -> None:
    if not request.user.is_authenticated:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
    if await email_domain_denied(session, request.user.email):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="email domain denied")


async def email_domain_denied(session: AsyncSession, email: str) -> bool:
    return not await repo.is_email_domain_allowed(session, email)


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
