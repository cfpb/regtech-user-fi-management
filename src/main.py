import logging
from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from routers import admin_router, institutions_router

from oauth2 import BearerTokenAuthBackend

from config import settings

log = logging.getLogger()

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exception: HTTPException) -> JSONResponse:
    log.error(exception, exc_info=True, stack_info=True)
    return JSONResponse(status_code=exception.status_code, content={"detail": exception.detail})


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exception: Exception) -> JSONResponse:
    log.error(exception, exc_info=True, stack_info=True)
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={"detail": "server error"},
    )


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.auth_url.unicode_string(), tokenUrl=settings.token_url.unicode_string()
)

app.add_middleware(AuthenticationMiddleware, backend=BearerTokenAuthBackend(oauth2_scheme))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["authorization"],
)

app.include_router(admin_router, prefix="/v1/admin")
app.include_router(institutions_router, prefix="/v1/institutions")
