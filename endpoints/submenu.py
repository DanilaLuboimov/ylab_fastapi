import http

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.submenu import MainSubmenu, SubmenuIn, SubmenuUpdate
from repositories.submenu import SubmenuRepository

from .depends import get_session, get_submenus_repository

router = APIRouter()


@router.post(
    '/{m_id}/submenus/',
    response_model=MainSubmenu,
    summary='Создать подменю',
    status_code=http.HTTPStatus.CREATED,
)
async def create_submenu(
        m_id: str,
        sm: SubmenuIn,
        submenus: SubmenuRepository = Depends(get_submenus_repository),
        session: AsyncSession = Depends(get_session),
) -> MainSubmenu:
    """
    Создает подменю, связанное с меню.
    :param m_id: id меню, в котором создается подменю.
    :param sm: поля с информацией о подменю.
    :param submenus: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await submenus.create(session=session, m_id=m_id, sm=sm)


@router.get(
    path='/{m_id}/submenus/',
    response_model=list[MainSubmenu],
    summary='Список меню',
    status_code=http.HTTPStatus.OK,
)
async def read_submenus(
        m_id: str,
        submenus: SubmenuRepository = Depends(get_submenus_repository),
        session: AsyncSession = Depends(get_session),
) -> list[MainSubmenu]:
    """
    Возвращает список подменю, связанных с меню.
    :param m_id: id меню, связанного с подменю.
    :param submenus: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await submenus.get_all(session=session, m_id=m_id)


@router.get(
    path='/{m_id}/submenus/{sm_id}',
    response_model=MainSubmenu,
    summary='Конкретное меню',
    status_code=http.HTTPStatus.OK,
)
async def read_submenu(
        m_id: str,
        sm_id: str,
        submenu: SubmenuRepository = Depends(get_submenus_repository),
        session: AsyncSession = Depends(get_session),
) -> MainSubmenu:
    """
    Возвращает подменю.
    :param m_id: id меню, связанного с подменю.
    :param sm_id: id подменю.
    :param submenu: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await submenu.get_by_id(session=session, m_id=m_id, sm_id=sm_id)


@router.patch(
    path='/{m_id}/submenus/{sm_id}',
    response_model=MainSubmenu,
    summary='Обновить подменю',
    status_code=http.HTTPStatus.OK,
)
async def update_submenu(
        m_id: str,
        sm_id: str,
        sm: SubmenuUpdate,
        submenus: SubmenuRepository = Depends(get_submenus_repository),
        session: AsyncSession = Depends(get_session),
) -> MainSubmenu:
    """
    Обновляет подменю
    :param m_id: id меню, связанного с подменю.
    :param sm_id: id подменю.
    :param sm: поля с информацией о меню для обновления.
    :param submenus: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await submenus.patch(session=session, m_id=m_id, sm_id=sm_id, sm=sm)


@router.delete(
    path='/{m_id}/submenus/{sm_id}',
    summary='Удалить подменю',
    status_code=http.HTTPStatus.OK,
)
async def delete_menu(
        m_id: str,
        sm_id: str,
        submenus: SubmenuRepository = Depends(get_submenus_repository),
        session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Удаляет подменю.
    :param m_id: id меню, связанного с подменю.
    :param sm_id: id подменю.
    :param submenus: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await submenus.delete(session=session, m_id=m_id, sm_id=sm_id)
