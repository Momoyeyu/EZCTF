import time
from typing import Any, Callable, TypeVar

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from common import erri
from common.security import verify_token

EXEMPT_PATHS: set[str] = set()
_EXEMPT_ENDPOINT_ATTR = "__jwt_exempt__"
_ROUTES_FROZEN_ATTR = "__jwt_routes_frozen__"
_SETUP_ATTR = "__jwt_middleware_installed__"

TFunc = TypeVar("TFunc", bound=Callable[..., Any])


def exempt(fn: TFunc) -> TFunc:
    setattr(fn, _EXEMPT_ENDPOINT_ATTR, True)
    return fn


def _build_exempt_paths(app: FastAPI) -> set[str]:
    paths: set[str] = set()
    for route in list(getattr(app, "router").routes):
        if not isinstance(route, APIRoute):
            continue
        if getattr(route.endpoint, _EXEMPT_ENDPOINT_ATTR, False):
            paths.add(route.path)
    return paths


def _freeze_route_registration(app: FastAPI) -> None:
    if getattr(app, _ROUTES_FROZEN_ATTR, False):
        return

    setattr(app, _ROUTES_FROZEN_ATTR, True)

    def _blocked(*_: object, **__: object):
        raise RuntimeError("Routes are frozen. Register all routes before setup_jwt_middleware.")

    app.include_router = _blocked
    app.add_api_route = _blocked
    app.add_route = _blocked
    app.mount = _blocked
    app.router.include_router = _blocked
    app.router.add_api_route = _blocked


def get_current_user_id(request: Request) -> int:
    state_user_id = getattr(request.state, "user_id", None)
    if state_user_id:
        return int(state_user_id)

    authorization = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
        payload = verify_token(token)
        sub = payload.get("sub")
        if sub:
            return int(sub)

    raise erri.unauthorized("Unauthorized")


def setup_jwt_middleware(app: FastAPI):
    if getattr(app, _SETUP_ATTR, False):
        return

    # Add default docs paths to exempt
    EXEMPT_PATHS.add("/docs")
    EXEMPT_PATHS.add("/redoc")
    EXEMPT_PATHS.add("/openapi.json")
    
    EXEMPT_PATHS.update(_build_exempt_paths(app))
    _freeze_route_registration(app)
    setattr(app, _SETUP_ATTR, True)

    @app.middleware("http")
    async def jwt_middleware(request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)
            
        path = request.url.path
        if path in EXEMPT_PATHS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
        
        token = auth_header.split(" ", 1)[1]
        try:
            payload = verify_token(token)
        except erri.BusinessError as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception:
             return JSONResponse(status_code=401, content={"detail": "Invalid token"})
             
        request.state.user_id = payload.get("sub")
        return await call_next(request)
