from http import HTTPStatus
from typing import Set
from fastapi import Request
from starlette.authentication import requires
from util import Router
from entities.models import UserProfile

from oauth2 import AuthenticatedUser, oauth2_admin

router = Router()


@router.get("/me/", response_model=AuthenticatedUser)
@requires("authenticated")
async def get_me(request: Request):
    return request.user


@router.put("/me/", status_code=HTTPStatus.ACCEPTED)
@requires("manage-account")
async def update_me(request: Request, user: UserProfile):
    oauth2_admin.update_user(request.user.id, user.get_user())
    if user.leis:
        oauth2_admin.associate_to_lei_set(request.user.id, user.leis)


@router.put("/me/groups/", status_code=HTTPStatus.ACCEPTED)
@requires("manage-account")
async def associate_group(request: Request, groups: Set[str]):
    for group in groups:
        oauth2_admin.associate_to_group(request.user.id, group)


@router.put("/me/institutions/", status_code=HTTPStatus.ACCEPTED)
@requires("manage-account")
async def associate_lei(request: Request, leis: Set[str]):
    oauth2_admin.associate_to_lei_set(request.user.id, leis)
