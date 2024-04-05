from enum import Enum
from typing import List

from pydantic import BaseModel

from src.config.database.database import sqlalchemy_to_pydantic, MenuOption, Order, User

MenuOptionModel = sqlalchemy_to_pydantic(MenuOption, amount_in_cart=(int, ...))

OrderModel = sqlalchemy_to_pydantic(Order)

ProfileModel = sqlalchemy_to_pydantic(User, orders=(List[OrderModel], ...))


class UpdateCartRequest(BaseModel):
    position_id: int
    amount: int


class CartModel(BaseModel):
    total_price: int
    positions: list[MenuOptionModel]


class ClaimWay(str, Enum):
    takeaway = 'takeaway'
    dine_in = 'dine_in'
