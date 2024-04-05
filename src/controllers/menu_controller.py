import datetime
from typing import Annotated, List

from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session

from .telegram_controller import bot
from ..config.database.database import MenuOption, User, sqlalchemy_to_pydantic, Cart, PositionInCart, Order
from ..support.dependencies import get_session, get_user_id
from ..support.schemas import MenuOptionModel, UpdateCartRequest, CartModel, ClaimWay, OrderModel

router = APIRouter(prefix="/menu", tags=['menu'])


@router.get('/positions', response_model=List[MenuOptionModel])
async def get_all_positions(category: str | None = None,
                            db_session: Session = Depends(get_session),
                            user_id: int = Depends(get_user_id)):
    positions_in_cart: List[PositionInCart] = db_session.query(Cart).filter(
        Cart.user_id == user_id).first().positions or []

    if category:
        positions = db_session.query(MenuOption).filter(MenuOption.category == category).all()
    else:
        positions = db_session.query(MenuOption).all()

    positions = [MenuOptionModel(**i.__dict__,
                                 amount_in_cart=next(
                                     (j.amount for j in positions_in_cart if j.position_id == i.id), 0)
                                 )
                 for i in positions]

    return positions


@router.get('/categories', response_model=List[str])
async def get_all_categories(db_session: Session = Depends(get_session)):
    categories = list(set([i.category for i in db_session.query(MenuOption).all()]))

    return categories


@router.get('/position', response_model=MenuOptionModel)
async def get_position_by_id(position_id: int,
                             db_session: Session = Depends(get_session),
                             user_id: int = Depends(get_user_id)):
    position = db_session.query(MenuOption).get(position_id)
    amount = next((i.amount for i in db_session.query(Cart).filter(Cart.user_id == user_id).first().positions), 0)

    return MenuOptionModel(**position.__dict__, amount_in_cart=amount)


@router.post('/update_cart', response_model=CartModel)
async def update_cart(update: UpdateCartRequest,
                      db_session: Session = Depends(get_session),
                      user_id: int = Depends(get_user_id)):
    cart = db_session.query(Cart).filter(Cart.user_id == user_id).first()

    if any(i.position_id == update.position_id for i in cart.positions):
        db_session.query(PositionInCart).filter(
            PositionInCart.cart_id == int(cart.id),
            PositionInCart.position_id == update.position_id
        ).update(
            {PositionInCart.amount: update.amount}
        )
    else:
        db_session.add(PositionInCart(position_id=update.position_id, amount=update.amount, cart_id=cart.id))

    db_session.commit()

    positions_in_cart: List[PositionInCart] = cart.positions

    positions = []
    total_price = 0

    for position_ic in positions_in_cart:
        menu_option: MenuOption = position_ic.position
        total_price += menu_option.price * position_ic.amount
        positions.append(MenuOptionModel(**menu_option.__dict__, amount_in_cart=position_ic.amount))

    return CartModel(total_price=total_price, positions=positions)


@router.get('/cart', response_model=CartModel)
async def get_cart_by_user_id(cart_id: int | None = None, db_session: Session = Depends(get_session),
                              user_id: int = Depends(get_user_id)):
    if cart_id:
        cart = db_session.query(Cart).filter(Cart.id == cart_id).first()
    else:
        cart = db_session.query(Cart).filter(Cart.user_id == user_id).first()

    positions_in_cart: List[PositionInCart] = cart.positions

    positions = []
    total_price = 0
    for position_ic in positions_in_cart:
        menu_option: MenuOption = position_ic.position
        total_price += menu_option.price * position_ic.amount
        positions.append(MenuOptionModel(**menu_option.__dict__, amount_in_cart=position_ic.amount))

    return CartModel(total_price=total_price, positions=positions)
