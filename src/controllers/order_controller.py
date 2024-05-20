import datetime
from typing import Annotated, List

from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session

from .telegram_controller import bot
from ..config.database.database import MenuOption, User, sqlalchemy_to_pydantic, Cart, PositionInCart, Order
from ..support.dependencies import get_session
from ..support.schemas import MenuOptionModel, UpdateCartRequest, CartModel, ClaimWay, OrderModel, \
    UserNotFoundException, OrderNotFoundException, EmptyCartException

router = APIRouter(prefix="/order", tags=['order'])


@router.get('/{user_id}/create_order', response_model=OrderModel)
async def create_order_from_user_cart(user_id: int, claim_way: ClaimWay,
                                      note: str | None = None,
                                      db_session: Session = Depends(get_session)):
    user = db_session.query(User).get(user_id)
    if not user:
        raise UserNotFoundException(user_id)

    cart = db_session.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart.postions:
        raise EmptyCartException(user_id)

    order = Order(user_id=user_id, cart_id=cart.id, claim_way=claim_way.value, note=note or 'Пусто')
    db_session.add(order)
    db_session.commit()

    return order


@router.get('/{user_id}/finish_order', response_model=bool)
async def finish_order_by_id(user_id: int, order_id: int, db_session: Session = Depends(get_session)):
    user = db_session.query(User).get(user_id)
    if not user:
        raise UserNotFoundException(user_id)

    db_session.query(Order).filter(Order.id == order_id).update(
        {
            Order.status: 'finished',
            Order.claim_time: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    )

    db_session.commit()
    # await bot.send_message(user_id, f'Заказ номер {order_id} готов к выдаче.')

    return True


@router.get('/get_order', response_model=OrderModel)
async def get_order_by_id(order_id: int, db_session: Session = Depends(get_session)):
    order = db_session.query(Order).get(order_id)

    if not order:
        raise OrderNotFoundException(order_id)

    return order


@router.get('/active_orders', response_model=list[OrderModel])
async def get_active_orders(db_session: Session = Depends(get_session)):
    orders = db_session.query(Order).filter(Order.status == 'processing').all()

    return orders
