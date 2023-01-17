from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from repositories.menu import MenuRepository
from .depends import get_menus_repository
from models.menu import Menu, MenuIn

router = APIRouter()


@router.get("/", response_model=list[Menu])
async def read_menus(menus: MenuRepository = Depends(get_menus_repository)):
    return await menus.get_all()


@router.get("/{m_id}", response_model=Menu)
async def read_menu(m_id: str,
                    menus: MenuRepository = Depends(get_menus_repository)):
    m = await menus.get_by_id(m_id)
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="menu not found")
    if m is None:
        raise not_found_exception
    return m


@router.post("/", response_model=Menu, status_code=201)
async def create_menu(m: MenuIn,
                 menus: MenuRepository = Depends(get_menus_repository)):
    return await menus.create(m)


@router.patch("/{m_id}", response_model=Menu)
async def update_menu(m_id: str, m: MenuIn,
                 menus: MenuRepository = Depends(get_menus_repository)):
    record = await menus.get_by_id(m_id)
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="menu not found")
    if record is None:
        raise not_found_exception
    return await menus.patch(m_id=m_id, m=m)


@router.delete("/{m_id}")
async def delete_menu(m_id: str,
                      menus: MenuRepository = Depends(get_menus_repository)):
    m = await menus.get_by_id(m_id=m_id)
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="menu not found")
    if m is None:
        raise not_found_exception

    await menus.delete(m_id=m_id)
    return {"status": True, "message": "The menu has been deleted"}
