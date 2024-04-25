from typing import Type, Dict, Any

from pydantic import create_model, BaseModel
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
from src.config.database.db_config import engine, Session

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    full_name = Column(String)
    cart = relationship('Cart')
    orders = relationship('Order')


class MenuOption(Base):
    __tablename__ = 'menu_options'
    id = Column(Integer(), primary_key=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String, default='дефолтное описание дефолтное описание дефолтное описание')
    img_source = Column(String, default='')
    positive_grades = Column(Integer, default=0)
    negative_grades = Column(Integer, default=0)
    note = Column(String, default='')
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category')


class PositionInCart(Base):
    __tablename__ = 'positions_in_carts'
    id = Column(Integer(), primary_key=True)
    position_id = Column(Integer, ForeignKey('menu_options.id'))
    cart_id = Column(Integer, ForeignKey('carts.id'))
    amount = Column(Integer, default=0)
    position = relationship('MenuOption')


class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    positions = relationship(PositionInCart)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', overlaps="orders")
    order_time = Column(String, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    cart_id = Column(Integer, ForeignKey('carts.id'))
    cart = relationship('Cart')
    claim_way = Column(String, default='')
    status = Column(String, default='processing')
    claim_time = Column(String, default='')
    note = Column(String, default='')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    menu_options = relationship('MenuOption')


def create_db():
    Base.metadata.create_all(bind=engine)


def sqlalchemy_to_pydantic(db_model: Type[Base], **field_definitions) -> Type[BaseModel]:
    annotations = {}

    for column in db_model.__table__.columns:
        python_type = column.type.python_type
        annotations[column.name] = (python_type, ...)

    for item_name, item_value in field_definitions.items():
        annotations[item_name] = item_value

    return create_model(
        db_model.__name__ + "Pydantic",
        __base__=BaseModel,
        **annotations,
    )


create_db()
