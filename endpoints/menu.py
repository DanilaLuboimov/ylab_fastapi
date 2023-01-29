import http

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.menu import MainMenu, MenuIn, MenuUpdate
from repositories.menu import MenuRepository

from .depends import get_menus_repository, get_session

router = APIRouter()


@router.get(
    path='/',
    response_model=list[MainMenu],
    summary='Список меню',
    status_code=http.HTTPStatus.OK,
)
async def read_menus(
        menus: MenuRepository = Depends(get_menus_repository),
        session: AsyncSession = Depends(get_session),
) -> list[MainMenu]:
    """
    Возвращает список всех меню.
    :param menus: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await menus.get_all(session=session)


@router.get(
    path='/{m_id}',
    response_model=MainMenu,
    summary='Конкретное меню',
    status_code=http.HTTPStatus.OK,
)
async def read_menu(
        m_id: str,
        menus: MenuRepository = Depends(get_menus_repository),
        session: AsyncSession = Depends(get_session),
) -> MainMenu:
    """
    Возвращает меню.
    :param m_id: id меню.
    :param menus: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await menus.get_by_id(session=session, m_id=m_id)


@router.post(
    path='/',
    response_model=MainMenu,
    summary='Создать меню',
    status_code=http.HTTPStatus.CREATED,
)
async def create_menu(
        m: MenuIn,
        menus: MenuRepository = Depends(get_menus_repository),
        session: AsyncSession = Depends(get_session),
) -> MainMenu:
    """
    Создает новое меню.
    :param m: поля с информацией о меню.
    :param menus: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await menus.create(session=session, m=m)


@router.patch(
    path='/{m_id}',
    response_model=MainMenu,
    summary='Обновить меню',
    status_code=http.HTTPStatus.OK,
)
async def update_menu(
        m_id: str,
        m: MenuUpdate,
        menus: MenuRepository = Depends(get_menus_repository),
        session: AsyncSession = Depends(get_session),
) -> MainMenu:
    """
    Обновляет меню.
    :param m_id: id меню
    :param m: поля с информацией о меню для обновления.
    :param menus: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await menus.patch(session=session, m_id=m_id, m=m)


@router.delete(
    path='/{m_id}',
    summary='Удалить меню',
    status_code=http.HTTPStatus.OK,
)
async def delete_menu(
        m_id: str,
        menus: MenuRepository = Depends(get_menus_repository),
        session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Удаляет меню.
    :param m_id: id меню.
    :param menus: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await menus.delete(session=session, m_id=m_id)
