from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from src.config.project_config import admin_password, admin_login
from src.support.dependencies import get_session
from src.support.schemas import Token, AuthenticationFailedException, RoleValidationFailedException, \
    PermissionsException

router = APIRouter(prefix='/auth', tags=['auth'])

SECRET_KEY = 'RWKwQJwBCiIzUWvh9TWsNr8spXnCQEhCwcbQQBDHTbo'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def authenticate_admin(username: str, password: str):
    if not username:
        return False
    return bcrypt_context.verify(password, bcrypt_context.hash(admin_password)) and username == admin_login


def create_access_token(username: str):
    encode = {'role': username}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post('/token', response_model=Token)
async def get_admin_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_admin(form_data.username, form_data.password):
        raise AuthenticationFailedException(form_data.username, form_data.password)

    token = create_access_token(form_data.username)

    return Token(access_token=token, token_type='bearer')


async def check_admin(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get('role')

        if not role:
            raise RoleValidationFailedException(token)
        if role != 'admin':
            raise PermissionsException(token, role, 'admin')

        return {'role': role}

    except JWTError:
        raise RoleValidationFailedException(token)
