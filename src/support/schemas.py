from enum import Enum
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status

from src.config.database.database import sqlalchemy_to_pydantic, MenuOption, Order, User, Category

MenuOptionModel = sqlalchemy_to_pydantic(MenuOption, amount_in_cart=(int, ...), category=(str, ...))

MenuOptionAdminModel = sqlalchemy_to_pydantic(MenuOption, category=(str, ...))

OrderModel = sqlalchemy_to_pydantic(Order)

ProfileModel = sqlalchemy_to_pydantic(User, orders=(List[OrderModel], ...))

CategoriesModel = sqlalchemy_to_pydantic(Category)


class UpdateCartRequest(BaseModel):
    position_id: int
    amount: int


class UpdateCategoryRequest(BaseModel):
    category_id: int | None
    name: str | None
    description: str | None


class CartModel(BaseModel):
    total_price: int
    positions: list[MenuOptionModel]


class UpdateMenuOptionRequest(BaseModel):
    id: int | None
    name: str | None
    price: int | None
    description: str | None
    img_source: str | None
    note: str | None
    category_id: int | None


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
            "error": "Position Amount Below Zero",
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
