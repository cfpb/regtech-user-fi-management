from http import HTTPStatus
from typing import Set
from fastapi import Depends, Request
from starlette.authentication import requires
from dependencies import check_domain
from util import Router
from entities.models import UserProfile

from entities.models import AuthenticatedUser
from oauth2 import oauth2_admin

router = Router()


@router.get("/me/", response_model=AuthenticatedUser)
@requires("authenticated")
def get_me(request: Request):
    return request.user


@router.put("/me/", status_code=HTTPStatus.ACCEPTED, dependencies=[Depends(check_domain)])
@requires("manage-account")
def update_me(request: Request, user: UserProfile):
    oauth2_admin.update_user(request.user.id, user.to_keycloak_user())
    if user.leis:
        oauth2_admin.associate_to_leis(request.user.id, user.leis)


@router.put("/me/institutions/", status_code=HTTPStatus.ACCEPTED, dependencies=[Depends(check_domain)])
@requires("manage-account")
def associate_lei(request: Request, leis: Set[str]):
    oauth2_admin.associate_to_leis(request.user.id, leis)
