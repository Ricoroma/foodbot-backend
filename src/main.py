import asyncio
import platform

import uvicorn
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
import os

from src.config.database.database import sqlalchemy_to_pydantic, User
from src.routes import get_apps_router

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(get_apps_router())

    return application


app = get_application()



