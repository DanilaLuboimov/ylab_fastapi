import http

from fastapi import APIRouter, Depends

from models.submenu import MainSubmenu, SubmenuIn, SubmenuUpdate
from services.submenu import SubmenuService

router = APIRouter()


@router.post(
    "/{m_id}/submenus/",
    response_model=MainSubmenu,
    summary="Создать подменю",
    status_code=http.HTTPStatus.CREATED,
)
async def create_submenu(
    m_id: str,
    sm: SubmenuIn,
    submenus: SubmenuService = Depends(),
) -> MainSubmenu:
    """
    Создает подменю, связанное с меню.
    :param m_id: id меню, в котором создается подменю.
    :param sm: поля с информацией о подменю.
    :param submenus: сервис для работы с логикой.
    """
    return await submenus.create(m_id=m_id, sm=sm)


@router.get(
    path="/{m_id}/submenus/",
    response_model=list[MainSubmenu],
    summary="Список меню",
    status_code=http.HTTPStatus.OK,
)
async def read_submenus(
    m_id: str,
    submenus: SubmenuService = Depends(),
) -> list[MainSubmenu]:
    """
    Возвращает список подменю, связанных с меню.
    :param m_id: id меню, связанного с подменю.
    :param submenus: сервис для работы с логикой.
    """
    return await submenus.get_all(m_id=m_id)


@router.get(
    path="/{m_id}/submenus/{sm_id}",
    response_model=MainSubmenu,
    summary="Конкретное меню",
    status_code=http.HTTPStatus.OK,
)
async def read_submenu(
    m_id: str,
    sm_id: str,
    submenu: SubmenuService = Depends(),
) -> MainSubmenu | dict:
    """
    Возвращает подменю.
    :param m_id: id меню, связанного с подменю.
    :param sm_id: id подменю.
    :param submenu: сервис для работы с логикой.
    """
    return await submenu.get_by_id(m_id=m_id, sm_id=sm_id)


@router.patch(
    path="/{m_id}/submenus/{sm_id}",
    response_model=MainSubmenu,
    summary="Обновить подменю",
    status_code=http.HTTPStatus.OK,
)
async def update_submenu(
    m_id: str,
    sm_id: str,
    sm: SubmenuUpdate,
    submenus: SubmenuService = Depends(),
) -> MainSubmenu | dict:
    """
    Обновляет подменю
    :param m_id: id меню, связанного с подменю.
    :param sm_id: id подменю.
    :param sm: поля с информацией о меню для обновления.
    :param submenus: сервис для работы с логикой.
    """
    return await submenus.patch(m_id=m_id, sm_id=sm_id, sm=sm)


@router.delete(
    path="/{m_id}/submenus/{sm_id}",
    summary="Удалить подменю",
    status_code=http.HTTPStatus.OK,
)
async def delete_menu(
    m_id: str,
    sm_id: str,
    submenus: SubmenuService = Depends(),
) -> dict:
    """
    Удаляет подменю.
    :param m_id: id меню, связанного с подменю.
    :param sm_id: id подменю.
    :param submenus: сервис для работы с логикой.
    """
    return await submenus.delete(m_id=m_id, sm_id=sm_id)
