from fastapi import APIRouter
from src.controllers import menu_controller, telegram_controller, order_controller, profile_controller


def get_apps_router():
    router = APIRouter()

    # router.include_router(admin_controller.router)
    router.include_router(menu_controller.router)
    router.include_router(telegram_controller.router)
    router.include_router(order_controller.router)
    router.include_router(profile_controller.router)

    return router
