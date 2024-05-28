import datetime
from copy import copy, deepcopy
from typing import Annotated, List

from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session

from .telegram_controller import bot
from ..config.database.database import MenuOption, User, sqlalchemy_to_pydantic, Cart, PositionInCart, Order
from ..support.dependencies import get_session
from ..support.schemas import MenuOptionModel, UpdateCartRequest, CartModel, ClaimWay, OrderModel, \
    UserNotFoundException, OrderNotFoundException, EmptyCartException

router = APIRouter(prefix="/order", tags=['order'])


@router.get('/{user_id}/create_order')
async def create_order_from_user_cart(user_id: int, claim_way: ClaimWay,
                                      note: str | None = None,
                                      db_session: Session = Depends(get_session)):
    user = db_session.query(User).get(user_id)
    if not user:
        raise UserNotFoundException(user_id)

    cart = db_session.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart.positions:
        raise EmptyCartException(user_id)

    order = Order(user_id=user_id, cart_id=cart.id, claim_way=claim_way.value, note=note or 'Пусто')
    db_session.add(order)
    db_session.commit()
    order = db_session.query(Order).get(order.id)

    positions = []
    for position_ic in cart.positions:
        menu_option: MenuOption = position_ic.position

        menu_option_dict = deepcopy(menu_option.__dict__)
        menu_option_dict['category'] = menu_option.category.name
        menu_option_dict['amount_in_cart'] = position_ic.amount

        positions.append(MenuOptionModel(
            **menu_option_dict)
        )

    order_model = OrderModel(**order.__dict__, positions=positions)

    cart.user_id = None
    new_cart = Cart(user_id=user_id)
    db_session.add(new_cart)
    db_session.commit()

    return order_model


@router.get('/finish_order', response_model=bool)
async def finish_order_by_id(order_id: int, db_session: Session = Depends(get_session)):
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

    positions = []
    for position_ic in order.cart.positions:
        menu_option: MenuOption = position_ic.position

        menu_option_dict = deepcopy(menu_option.__dict__)
        menu_option_dict['category'] = menu_option.category.name
        menu_option_dict['amount_in_cart'] = position_ic.amount

        positions.append(MenuOptionModel(
            **menu_option_dict)
        )

    return OrderModel(**order.__dict__, positions=positions)


@router.get('/active_orders', response_model=list[OrderModel])
async def get_active_orders(db_session: Session = Depends(get_session)):
    orders = db_session.query(Order).filter(Order.status == 'processing').all()

    orders_models = []
    for order in orders:
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

    return orders_models
