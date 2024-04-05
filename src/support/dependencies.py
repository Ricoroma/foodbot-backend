from fastapi import HTTPException
from fastapi.params import Header

from src.config.database.db_config import Session


def get_session():
    with Session() as db_session:
        yield db_session
