from repositories.menu import MenuRepository
from repositories.submenu import SubmenuRepository
from repositories.dish import DishRepository
from db.base import database


def get_menus_repository() -> MenuRepository:
    return MenuRepository(database)


def get_submenus_repository() -> SubmenuRepository:
    return SubmenuRepository(database)


def get_dishes_repository() -> DishRepository:
    return DishRepository(database)
