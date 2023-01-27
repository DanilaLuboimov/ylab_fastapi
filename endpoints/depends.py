from db.base import database
from repositories.dish import DishRepository
from repositories.menu import MenuRepository
from repositories.submenu import SubmenuRepository


def get_menus_repository() -> MenuRepository:
    return MenuRepository(database)


def get_submenus_repository() -> SubmenuRepository:
    return SubmenuRepository(database)


def get_dishes_repository() -> DishRepository:
    return DishRepository(database)
