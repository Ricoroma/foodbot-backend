from pydantic import BaseModel

from src.config.database.database import sqlalchemy_to_pydantic, MenuOption

MenuOptionModel = sqlalchemy_to_pydantic(MenuOption, amount_in_cart=(int, ...))


class UpdateCartRequest(BaseModel):
    position_id: int
    amount: int


class CartModel(BaseModel):
    total_price: int
    positions: list[MenuOptionModel]
