from typing import Generator

from db.base import async_session
from repositories.dish import DishRepository
from repositories.menu import MenuRepository
from repositories.submenu import SubmenuRepository


def get_menus_repository() -> MenuRepository:
    return MenuRepository()


def get_submenus_repository() -> SubmenuRepository:
    return SubmenuRepository()


def get_dishes_repository() -> DishRepository:
    return DishRepository()


async def get_session() -> Generator:
    async with async_session() as session:
        async with session.begin():
            yield session
