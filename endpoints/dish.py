from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from repositories.dish import DishRepository
from .depends import get_dishes_repository
from models.dish import Dish, DishIn

router = APIRouter()


@router.get("/{m_id}/submenus/{sm_id}/dishes/", response_model=list[Dish])
async def read_dishes(m_id: str, sm_id: str,
                      dishes: DishRepository = Depends(get_dishes_repository)):
    return await dishes.get_all(m_id, sm_id)


@router.get("/{m_id}/submenus/{sm_id}/dishes/{d_id}", response_model=Dish)
async def read_dish(m_id: str, sm_id: str, d_id: str,
                    dishes: DishRepository = Depends(get_dishes_repository)):
    d = await dishes.get_by_id(d_id)
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="dish not found")
    if d is None:
        raise not_found_exception
    return d


@router.post("/{m_id}/submenus/{sm_id}/dishes/", response_model=Dish,
             status_code=201)
async def create_dish(m_id: str, sm_id: str, d: DishIn,
                      dishes: DishRepository = Depends(get_dishes_repository)):
    return await dishes.create(m_id, sm_id, d)


@router.patch("/{m_id}/submenus/{sm_id}/dishes/{d_id}", response_model=Dish)
async def update_dish(m_id: str, sm_id: str, d_id: str, d: DishIn,
                      dish: DishRepository = Depends(get_dishes_repository)):
    record = await dish.get_by_id(d_id)
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="dish not found")
    if record is None:
        raise not_found_exception
    return await dish.patch(d_id, d)


@router.delete("/{m_id}/submenus/{sm_id}/dishes/{d_id}")
async def delete_dish(m_id: str, sm_id: str, d_id: str,
                      dishes: DishRepository = Depends(get_dishes_repository)):
    d = await dishes.get_by_id(d_id)
    not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="dish not found")
    if d is None:
        raise not_found_exception

    await dishes.delete(d_id)
    return {"status": True, "message": "The dish has been deleted"}
