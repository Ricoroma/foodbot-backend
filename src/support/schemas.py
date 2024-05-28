from enum import Enum
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status

from src.config.database.database import sqlalchemy_to_pydantic, MenuOption, Order, User, Category

MenuOptionModel = sqlalchemy_to_pydantic(MenuOption, amount_in_cart=(int, ...), category=(str, ...))

MenuOptionAdminModel = sqlalchemy_to_pydantic(MenuOption, category=(str, ...))

OrderModel = sqlalchemy_to_pydantic(Order, positions=(List[MenuOptionModel], ...))

ProfileModel = sqlalchemy_to_pydantic(User, orders=(List[OrderModel], ...))

CategoriesModel = sqlalchemy_to_pydantic(Category)


class UpdateCartRequest(BaseModel):
    position_id: int
    amount: int


class UpdateCategoryRequest(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None


class CartModel(BaseModel):
    total_price: int
    positions: list[MenuOptionModel]


class UpdateMenuOptionRequest(BaseModel):
    id: int | None = None
    name: str | None = None
    price: int | None = None
    description: str | None = None
    img_source: str | None = None
    note: str | None = None
    category_id: int | None = None


class ClaimWay(str, Enum):
    takeaway = 'takeaway'
    dine_in = 'dine_in'


class UserNotFoundException(HTTPException):
    def __init__(self, user_id: int):
        self.detail = {
            "error": "User Not Found",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "user_id": user_id
        }
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=self.detail)


class CategoryNotFoundException(HTTPException):
    def __init__(self, category: int):
        self.detail = {
            "error": "Category Not Found",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "category_id": category
        }
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=self.detail)


class PositionNotFoundException(HTTPException):
    def __init__(self, position_id: int):
        self.detail = {
            "error": "Position Not Found",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "position_id": position_id
        }
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=self.detail)


class UpdateCartException(HTTPException):
    def __init__(self, position_id: int, amount: int):
        self.detail = {
            "error": "Position Amount Below Zero Or Position Not Found",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "position_id": position_id,
            "amount": amount
        }
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=self.detail)


class EmptyCartException(HTTPException):
    def __init__(self, user_id: int):
        self.detail = {
            "error": "No Items In Cart",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "user_id": user_id,
        }
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=self.detail)


class OrderNotFoundException(HTTPException):
    def __init__(self, order_id: int):
        self.detail = {
            "error": "User Not Found",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "order_id": order_id
        }
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=self.detail)


class UpdateErrorException(HTTPException):
    def __init__(self, error, params: dict):
        self.detail = {
            "error": error,
            "status_code": status.HTTP_400_BAD_REQUEST,
            **params
        }
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=self.detail)


class AuthenticationFailedException(HTTPException):
    def __init__(self, username: str, password: str):
        self.detail = {
            "error": 'Authentication Failed',
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "username": username,
            "password": password
        }
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=self.detail)


class RoleValidationFailedException(HTTPException):
    def __init__(self, token: str):
        self.detail = {
            "error": 'Role Validation Failed',
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "token": token
        }
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=self.detail)


class PermissionsException(HTTPException):
    def __init__(self, token: str, role: str, required_role: str):
        self.detail = {
            "error": 'Lack Of Permissions',
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "token": token,
            "role": role,
            "required_role": required_role
        }
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=self.detail)


class Token(BaseModel):
    access_token: str
    token_type: str
