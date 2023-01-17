from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from repositories.submenu import SubmenuRepository
from .depends import get_submenus_repository
from models.submenu import Submenu, SubmenuIn

router = APIRouter()


@router.post("/{m_id}/submenus/", response_model=Submenu, status_code=201)
async def create_submenu(m_id: str, sm: SubmenuIn,
                         submenus: SubmenuRepository = Depends(
                             get_submenus_repository)):
    return await submenus.create(m_id, sm)


@router.get("/{m_id}/submenus/", response_model=list[Submenu])
async def read_submenus(m_id: str,
                        submenus: SubmenuRepository = Depends(
                            get_submenus_repository)):
    return await submenus.get_all(m_id)


@router.get("/{m_id}/submenus/{sm_id}", response_model=Submenu)
async def read_submenu(m_id: str, sm_id: str,
                       submenu: SubmenuRepository = Depends(
                           get_submenus_repository)):
    sm = await submenu.get_by_id(m_id, sm_id)
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="submenu not found")

    if sm is None:
        raise not_found_exception
    return sm


@router.patch("/{m_id}/submenus/{sm_id}", response_model=Submenu)
async def update_submenu(m_id: str, sm_id: str, sm: SubmenuIn,
                         menus: SubmenuRepository = Depends(
                             get_submenus_repository)):
    record = await menus.get_by_id(m_id, sm_id)
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="Menu not found")
    if record is None:
        raise not_found_exception
    return await menus.patch(m_id, sm_id, sm)


@router.delete("/{m_id}/submenus/{sm_id}")
async def delete_menu(m_id: str, sm_id: str,
                      submenus: SubmenuRepository = Depends(
                          get_submenus_repository)):
    m = await submenus.get_by_id(m_id, sm_id)
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="Submenu not found")
    if m is None:
        raise not_found_exception

    await submenus.delete(sm_id)
    return {"status": True, "message": "The submenu has been deleted"}
