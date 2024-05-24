import asyncio
import logging
import platform
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.config.project_config import webhook_url
from src.controllers.telegram_controller import dp, bot

from src.routes import get_apps_router, setup_exceptions_handlers
from tgbot.handlers import main_handler, admin_handler
from tgbot.middlewares.database_middleware import DatabaseMiddleware

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('start')
    dp.include_router(main_handler.router)
    dp.include_router(admin_handler.router)

    dp.update.middleware(DatabaseMiddleware())

    await bot.set_webhook(webhook_url)

    yield

    await bot.delete_webhook(drop_pending_updates=True)

    session = bot.session
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
    application = setup_exceptions_handlers(application)
    application.mount("/static", StaticFiles(directory="static"), name="static")

    return application


app = get_application()

# uvicorn.run(app)
