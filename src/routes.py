from fastapi import APIRouter
from src.controllers import menu_controller


def get_apps_router():
    router = APIRouter()

    # router.include_router(admin_controller.router)
    router.include_router(menu_controller.router)
    return router
