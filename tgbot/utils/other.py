from src.config.database.database import MenuOption


def format_position(position: MenuOption):
    text = f'Категория {position.category.name}\n' \
           f'Название: {position.name}\n' \
           f'Описание: {position.description}\n' \
           f'Цена: {position.price}₽\n' \
           f'Пометка: {position.note}\n'
    return text
