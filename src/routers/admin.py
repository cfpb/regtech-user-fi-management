from http import HTTPStatus
from typing import Set
from fastapi import Depends, Request
from starlette.authentication import requires
from dependencies import check_domain

from regtech_api_commons.api import Router
from entities.models import UserProfile

from regtech_api_commons.models import RegTechUser
from regtech_api_commons.oauth2 import OAuth2Admin
from config import kc_settings

router = Router()

oauth2_admin = OAuth2Admin(kc_settings)


@router.get("/me/", response_model=RegTechUser)
@requires("authenticated")
def get_me(request: Request):
    return oauth2_admin.get_user(request.user.id)


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
