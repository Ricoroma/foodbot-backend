from fastapi import HTTPException
from fastapi.params import Header

from src.config.database.db_config import Session


async def get_user_id(user_id: str = Header(...)):
    if user_id is None:
        raise HTTPException(status_code=400, detail="UserId header missing")
    return user_id


def get_session():
    with Session() as db_session:
        yield db_session
