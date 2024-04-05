import datetime
from typing import Annotated, List

from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session

from .telegram_controller import bot
from ..config.database.database import MenuOption, User, sqlalchemy_to_pydantic, Cart, PositionInCart, Order
from ..support.dependencies import get_session, get_user_id
from ..support.schemas import MenuOptionModel, UpdateCartRequest, CartModel, ClaimWay, OrderModel, ProfileModel

router = APIRouter(prefix="/profile", tags=['profile'])


@router.get('/', response_model=ProfileModel)
async def get_profile_by_id(db_session: Session = Depends(get_session),
                            user_id: int = Depends(get_user_id)):
    user = db_session.query(User).get(user_id)
    return ProfileModel(**user.__dict__, orders=[OrderModel(**i.__dict__) for i in user.orders])
