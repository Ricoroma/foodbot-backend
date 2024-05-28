import datetime
from copy import deepcopy
from typing import Annotated, List

from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session

from .telegram_controller import bot
from ..config.database.database import MenuOption, User, sqlalchemy_to_pydantic, Cart, PositionInCart, Order
from ..support.dependencies import get_session
from ..support.schemas import MenuOptionModel, UpdateCartRequest, CartModel, ClaimWay, OrderModel, ProfileModel, \
    UserNotFoundException

router = APIRouter(prefix="/profile", tags=['profile'])


@router.get('/{user_id}', response_model=ProfileModel)
async def get_profile_by_id(user_id: int, db_session: Session = Depends(get_session)):
    user = db_session.query(User).get(user_id)
    if not user:
        raise UserNotFoundException(user_id)

    user: User = db_session.query(User).get(user_id)
    orders_models = []
    for order in user.orders:
        positions = []
        for position_ic in order.cart.positions:
            menu_option: MenuOption = position_ic.position

            menu_option_dict = deepcopy(menu_option.__dict__)
            menu_option_dict['category'] = menu_option.category.name
            menu_option_dict['amount_in_cart'] = position_ic.amount

            positions.append(MenuOptionModel(
                **menu_option_dict)
            )

        orders_models.append(OrderModel(**order.__dict__, positions=positions))

    user_dict = deepcopy(user.__dict__)
    user_dict['orders'] = orders_models

    return ProfileModel(**user_dict)
