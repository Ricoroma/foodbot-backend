import datetime
from typing import Annotated, List

from fastapi import Depends, HTTPException, Query, APIRouter
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from .telegram_controller import bot
from ..config.database.database import MenuOption, User, sqlalchemy_to_pydantic, Cart, PositionInCart, Order
from ..support.dependencies import get_session
from ..support.schemas import UserNotFoundException, CategoryNotFoundException, PositionNotFoundException, \
    UpdateCartException, EmptyCartException, OrderNotFoundException, UpdateErrorException, \
    AuthenticationFailedException, RoleValidationFailedException, PermissionsException


async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def category_not_found_exception_handler(request: Request, exc: CategoryNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def position_not_found_exception_handler(request: Request, exc: PositionNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def update_cart_exception_handler(request: Request, exc: UpdateCartException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def empty_cart_exception_handler(request: Request, exc: EmptyCartException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def order_not_found_exception_handler(request: Request, exc: OrderNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def update_error_exception_handler(request: Request, exc: UpdateErrorException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def authentication_failed_exception_handler(request: Request, exc: AuthenticationFailedException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def role_validation_failed_exception_handler(request: Request, exc: RoleValidationFailedException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


async def permissions_exception_handler(request: Request, exc: PermissionsException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )
