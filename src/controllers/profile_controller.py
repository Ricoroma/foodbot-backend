import datetime
from typing import Annotated, List

from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session

from .telegram_controller import bot
from ..config.database.database import MenuOption, User, sqlalchemy_to_pydantic, Cart, PositionInCart, Order
from ..support.dependencies import get_session
from ..support.schemas import MenuOptionModel, UpdateCartRequest, CartModel, ClaimWay, OrderModel, ProfileModel

router = APIRouter(prefix="/profile", tags=['profile'])


@router.get('/{user_id}', response_model=ProfileModel)
async def get_profile_by_id(user_id: int, db_session: Session = Depends(get_session)):
    user = db_session.query(User).get(user_id)
    return ProfileModel(**user.__dict__, orders=[OrderModel(**i.__dict__) for i in user.orders])
