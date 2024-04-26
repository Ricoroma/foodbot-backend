from fastapi import APIRouter, FastAPI
from src.controllers import menu_controller, telegram_controller, order_controller, profile_controller, admin_controller
from src.controllers.exceptions_controller import user_not_found_exception_handler, \
    category_not_found_exception_handler, position_not_found_exception_handler, update_cart_exception_handler, \
    empty_cart_exception_handler
from src.support.schemas import UserNotFoundException, CategoryNotFoundException, PositionNotFoundException


def get_apps_router():
    router = APIRouter()

    router.include_router(admin_controller.router)
    router.include_router(menu_controller.router)
    router.include_router(telegram_controller.router)
    router.include_router(order_controller.router)
    router.include_router(profile_controller.router)

    return router


def setup_exceptions_handlers(app: FastAPI):
    app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
    app.add_exception_handler(CategoryNotFoundException, category_not_found_exception_handler)
    app.add_exception_handler(PositionNotFoundException, position_not_found_exception_handler)
    app.add_exception_handler(PositionNotFoundException, update_cart_exception_handler)
    app.add_exception_handler(PositionNotFoundException, empty_cart_exception_handler)

    return app
