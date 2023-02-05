from typing import AsyncGenerator

from db.base import async_session
from repositories.dish import DishRepository
from repositories.files import FileRepository
from repositories.menu import MenuRepository
from repositories.submenu import SubmenuRepository
from repositories.test_data import TestDataRepository


def get_menus_repository() -> MenuRepository:
    return MenuRepository()


def get_submenus_repository() -> SubmenuRepository:
    return SubmenuRepository()


def get_dishes_repository() -> DishRepository:
    return DishRepository()


def get_files_repository() -> FileRepository:
    return FileRepository()


def get_test_data_repository() -> TestDataRepository:
    return TestDataRepository()


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        async with session.begin():
            yield session
