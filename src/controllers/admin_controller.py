import datetime
from typing import Annotated, List

from fastapi import Depends, HTTPException, Query, APIRouter
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from .telegram_controller import bot
from ..config.database.database import MenuOption, User, sqlalchemy_to_pydantic, Cart, PositionInCart, Order, Category
from ..support.dependencies import get_session
from ..support.schemas import MenuOptionModel, UpdateCartRequest, CartModel, UserNotFoundException, \
    PositionNotFoundException, CategoryNotFoundException, UpdateCartException, CategoriesModel, UpdateCategoryRequest, \
    MenuOptionAdminModel, UpdateMenuOptionRequest

router = APIRouter(prefix="/admin", tags=['admin'])


@router.post('/category', response_model=list[CategoriesModel])
async def add_or_change_category_handler(update: UpdateCategoryRequest, db_session: Session = Depends(get_session)):
    category: Category = db_session.query(Category).get(update.category_id)
    if not category:
        db_session.add(Category(name=update.name, description=update.description))
    else:
        if update.name:
            category.name = update.name
        if update.description:
            category.description = update.description

    db_session.commit()

    categories = db_session.query(Category).all()

    return categories


@router.post('/position', response_model=list[MenuOptionAdminModel])
async def update_menu_option(update: UpdateMenuOptionRequest, db_session: Session = Depends(get_session)):
    position: MenuOption = db_session.query(MenuOption).get(update.id)

    if not position:
        db_session.add(MenuOption(name=update.name, price=update.price, description=update.description,
                                  category_id=update.category_id, note=update.note, img_source=update.img_source))
    else:
        if update.name:
            position.name = update.name
        if update.description:
            position.description = update.description
        if update.price:
            position.price = update.price
        if update.img_source:
            position.img_source = update.img_source
        if update.name:
            position.name = update.name
        if update.category_id:
            position.category_id = update.category_id

    db_session.commit()

    positions = db_session.query(MenuOption).all()

    return [MenuOptionAdminModel(**i.__dict__, category=i.category.name) for i in positions]
