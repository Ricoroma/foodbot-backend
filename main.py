import asyncio
import logging
import platform
from contextlib import asynccontextmanager

import uvicorn
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from aiogram import Bot, Dispatcher, types
import os

from src.config.database.database import sqlalchemy_to_pydantic, User
from src.config.project_config import webhook_url
from src.controllers.telegram_controller import dp, bot
from src.routes import get_apps_router
from tgbot.handlers import main_handler
from tgbot.middlewares.database_middleware import DatabaseMiddleware

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('start')
    dp.include_router(main_handler.router)
    # dp.include_router(admin_handler.router)
    # dp.include_router(traders_handler.router)

    dp.update.middleware(DatabaseMiddleware())

    await bot.set_webhook(webhook_url)

    yield

    await bot.delete_webhook(drop_pending_updates=True)

    session = await bot.get_session()
    await session.close()


def get_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    application.include_router(get_apps_router())
    application.add_middleware(CORSMiddleware,
                               allow_origins=["*"],
                               allow_credentials=True,
                               allow_methods=["*"],
                               allow_headers=["*"],
                               )

    return application


app = get_application()
