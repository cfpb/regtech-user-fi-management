from typing import Set
from fastapi import Depends, Request
from starlette.authentication import requires
from regtech_user_fi_management.dependencies import check_domain

from regtech_api_commons.api.router_wrapper import Router
from regtech_user_fi_management.entities.models.dto import UserProfile

from regtech_api_commons.models.auth import RegTechUser
from regtech_api_commons.oauth2.oauth2_admin import OAuth2Admin
from regtech_user_fi_management.config import kc_settings

router = Router()

oauth2_admin = OAuth2Admin(kc_settings)


@router.get("/me/", response_model=RegTechUser)
@requires("authenticated")
def get_me(request: Request):
    return oauth2_admin.get_user(request.user.id)


@router.put("/me/", response_model=RegTechUser, dependencies=[Depends(check_domain)])
@requires("manage-account")
def update_me(request: Request, user: UserProfile):
    oauth2_admin.update_user(request.user.id, user.to_keycloak_user())
    if user.leis:
        oauth2_admin.associate_to_leis(request.user.id, user.leis)
    return oauth2_admin.get_user(request.user.id)


@router.put("/me/institutions/", response_model=RegTechUser, dependencies=[Depends(check_domain)])
@requires("manage-account")
def associate_lei(request: Request, leis: Set[str]):
    oauth2_admin.associate_to_leis(request.user.id, leis)
    return oauth2_admin.get_user(request.user.id)
