import http

from fastapi import APIRouter, Depends

from models.menu import MainMenu, MenuIn, MenuUpdate
from services.menu import MenuService

router = APIRouter()


@router.get(
    path="/",
    response_model=list[MainMenu],
    summary="Список меню",
    status_code=http.HTTPStatus.OK,
)
async def read_menus(
    menus: MenuService = Depends(),
) -> list[MainMenu]:
    """
    Возвращает список всех меню.
    :param menus: сервис для работы с логикой.
    """
    return await menus.get_all()


@router.get(
    path="/{m_id}",
    response_model=MainMenu,
    summary="Конкретное меню",
    status_code=http.HTTPStatus.OK,
)
async def read_menu(
    m_id: str,
    menus: MenuService = Depends(),
) -> MainMenu | dict:
    """
    Возвращает меню.
    :param m_id: id меню.
    :param menus: сервис для работы с логикой.
    """
    return await menus.get_by_id(m_id=m_id)


@router.post(
    path="/",
    response_model=MainMenu,
    summary="Создать меню",
    status_code=http.HTTPStatus.CREATED,
)
async def create_menu(
    m: MenuIn,
    menus: MenuService = Depends(),
) -> MainMenu:
    """
    Создает новое меню.
    :param m: поля с информацией о меню.
    :param menus: сервис для работы с логикой.
    """
    return await menus.create(m=m)


@router.patch(
    path="/{m_id}",
    response_model=MainMenu,
    summary="Обновить меню",
    status_code=http.HTTPStatus.OK,
)
async def update_menu(
    m_id: str,
    m: MenuUpdate,
    menus: MenuService = Depends(),
) -> MainMenu | dict:
    """
    Обновляет меню.
    :param m_id: id меню
    :param m: поля с информацией о меню для обновления.
    :param menus: сервис для работы с логикой.
    """
    return await menus.patch(m_id=m_id, m=m)


@router.delete(
    path="/{m_id}",
    summary="Удалить меню",
    status_code=http.HTTPStatus.OK,
)
async def delete_menu(
    m_id: str,
    menus: MenuService = Depends(),
) -> dict:
    """
    Удаляет меню.
    :param m_id: id меню.
    :param menus: сервис для работы с логикой.
    """
    return await menus.delete(m_id=m_id)
