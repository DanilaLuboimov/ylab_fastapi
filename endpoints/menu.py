import http

from fastapi import APIRouter, Depends

from models.menu import Menu, MenuIn
from repositories.menu import MenuRepository

from .depends import get_menus_repository

router = APIRouter()


@router.get(
    path='/',
    response_model=list[Menu],
    summary='Список меню',
    status_code=http.HTTPStatus.OK,
)
async def read_menus(
        menus: MenuRepository = Depends(get_menus_repository),
) -> list[Menu]:
    """
    Возвращает список всех меню.
    :param menus: репозиторий для работы с логикой.
    """
    return await menus.get_all()


@router.get(
    path='/{m_id}',
    response_model=Menu,
    summary='Конкретное меню',
    status_code=http.HTTPStatus.OK,
)
async def read_menu(
        m_id: str,
        menus: MenuRepository = Depends(get_menus_repository),
) -> Menu:
    """
    Возвращает меню.
    :param m_id: id меню.
    :param menus: репозиторий для работы с логикой.
    """
    return await menus.get_by_id(m_id)


@router.post(
    path='/',
    response_model=Menu,
    summary='Создать меню',
    status_code=http.HTTPStatus.CREATED,
)
async def create_menu(
        m: MenuIn,
        menus: MenuRepository = Depends(get_menus_repository),
) -> Menu:
    """
    Создает новое меню.
    :param m: поля с информацией о меню.
    :param menus: репозиторий для работы с логикой.
    """
    return await menus.create(m)


@router.patch(
    path='/{m_id}',
    response_model=Menu,
    summary='Обновить меню',
    status_code=http.HTTPStatus.OK,
)
async def update_menu(
        m_id: str, m: MenuIn,
        menus: MenuRepository = Depends(get_menus_repository),
) -> Menu:
    """
    Обновляет меню.
    :param m_id: id меню
    :param m: поля с информацией о меню для обновления.
    :param menus: репозиторий для работы с логикой.
    """
    return await menus.patch(m_id=m_id, m=m)


@router.delete(
    path='/{m_id}',
    summary='Удалить меню',
    status_code=http.HTTPStatus.OK,
)
async def delete_menu(
        m_id: str,
        menus: MenuRepository = Depends(get_menus_repository),
) -> dict:
    """
    Удаляет меню.
    :param m_id: id меню.
    :param menus: репозиторий для работы с логикой.
    """
    return await menus.delete(m_id=m_id)
