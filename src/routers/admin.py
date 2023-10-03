from http import HTTPStatus
from typing import Dict, Any, Set
from fastapi import Depends, Request
from starlette.authentication import requires
from dependencies import check_domain
from util import Router

from entities.models import AuthenticatedUser
from oauth2 import oauth2_admin

router = Router()


@router.get("/me/", response_model=AuthenticatedUser)
@requires("authenticated")
async def get_me(request: Request):
    return request.user


@router.put("/me/", status_code=HTTPStatus.ACCEPTED, dependencies=[Depends(check_domain)])
@requires("manage-account")
async def update_me(request: Request, user: Dict[str, Any]):
    oauth2_admin.update_user(request.user.id, user)


@router.put("/me/institutions/", status_code=HTTPStatus.ACCEPTED, dependencies=[Depends(check_domain)])
@requires("manage-account")
async def associate_lei(request: Request, leis: Set[str]):
    for lei in leis:
        oauth2_admin.associate_to_lei(request.user.id, lei)
