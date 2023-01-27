import http

from fastapi import APIRouter, Depends

from models.submenu import Submenu, SubmenuIn
from repositories.submenu import SubmenuRepository

from .depends import get_submenus_repository

router = APIRouter()


@router.post(
    '/{m_id}/submenus/',
    response_model=Submenu,
    summary='Создать подменю',
    status_code=http.HTTPStatus.CREATED,
)
async def create_submenu(
        m_id: str,
        sm: SubmenuIn,
        submenus: SubmenuRepository = Depends(get_submenus_repository),
) -> Submenu:
    """
    Создает подменю, связанное с меню.
    :param m_id: id меню, в котором создается подменю.
    :param sm: поля с информацией о подменю.
    :param submenus: репозиторий для работы с логикой.
    """
    return await submenus.create(m_id, sm)


@router.get(
    path='/{m_id}/submenus/',
    response_model=list[Submenu],
    summary='Список меню',
    status_code=http.HTTPStatus.OK,
)
async def read_submenus(
        m_id: str,
        submenus: SubmenuRepository = Depends(get_submenus_repository),
) -> list[Submenu]:
    """
    Возвращает список подменю, связанных с меню.
    :param m_id: id меню, связанного с подменю.
    :param submenus: репозиторий для работы с логикой.
    """
    return await submenus.get_all(m_id)


@router.get(
    path='/{m_id}/submenus/{sm_id}',
    response_model=Submenu,
    summary='Конкретное меню',
    status_code=http.HTTPStatus.OK,
)
async def read_submenu(
        m_id: str,
        sm_id: str,
        submenu: SubmenuRepository = Depends(get_submenus_repository),
) -> Submenu:
    """
    Возвращает подменю.
    :param m_id: id меню, связанного с подменю.
    :param sm_id: id подменю.
    :param submenu: репозиторий для работы с логикой.
    """
    return await submenu.get_by_id(m_id, sm_id)


@router.patch(
    path='/{m_id}/submenus/{sm_id}',
    response_model=Submenu,
    summary='Обновить подменю',
    status_code=http.HTTPStatus.OK,
)
async def update_submenu(
        m_id: str,
        sm_id: str,
        sm: SubmenuIn,
        submenus: SubmenuRepository = Depends(get_submenus_repository),
) -> Submenu:
    """
    Обновляет подменю
    :param m_id: id меню, связанного с подменю.
    :param sm_id: id подменю.
    :param sm: поля с информацией о меню для обновления.
    :param submenus: репозиторий для работы с логикой.
    """
    return await submenus.patch(m_id, sm_id, sm)


@router.delete(
    path='/{m_id}/submenus/{sm_id}',
    summary='Удалить подменю',
    status_code=http.HTTPStatus.OK,
)
async def delete_menu(
        m_id: str,
        sm_id: str,
        submenus: SubmenuRepository = Depends(get_submenus_repository),
) -> dict:
    """
    Удаляет подменю.
    :param m_id: id меню, связанного с подменю.
    :param sm_id: id подменю.
    :param submenus: репозиторий для работы с логикой.
    """
    return await submenus.delete(m_id, sm_id)
