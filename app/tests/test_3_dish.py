import os

import pytest
from sqlalchemy import delete

from db.tables import Dish


@pytest.mark.asyncio
async def test_create_dish(async_client, event_loop, async_session):
    title = "TEST dish 1"
    description = "TEST dish description 1"
    data = {
        "title": title,
        "description": description,
        "price": "13",
    }
    url = f'{os.getenv("MENU_ID")}/submenus/{os.getenv("SUBMENU_ID")}/dishes/'
    response = await async_client.post(f"/api/v1/menus/{url}", json=data)
    assert response.status_code == 201
    res_data = response.json()
    assert res_data.get("title") == title
    assert res_data.get("description") == description
    assert res_data.get("price") == "13.00"
    stmt = delete(Dish).where(Dish.id == res_data.get("id"))

    async with async_session.begin():
        await async_session.execute(stmt)


@pytest.mark.asyncio
async def test_get_one_dish(async_client, event_loop):
    url = f'{os.getenv("MENU_ID")}/submenus/{os.getenv("SUBMENU_ID")}/dishes/{os.getenv("DISH_ID")}'
    response = await async_client.get(f"/api/v1/menus/{url}")
    assert response.status_code == 200
    res_data = response.json()

    assert res_data.get("title") == "TEST dish 1"
    assert res_data.get("description") == "TEST dish description 1"
    assert res_data.get("price") == "13.35"

    url = url[:-1] + "0"
    response = await async_client.get(f"/api/v1/menus/{url}")
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}


@pytest.mark.asyncio
async def test_get_all_dishes(async_client, event_loop):
    url = f'{os.getenv("MENU_ID")}/submenus/{os.getenv("SUBMENU_ID")}/dishes/'
    response = await async_client.get(f"/api/v1/menus/{url}")
    assert response.status_code == 200
    res_data = response.json()
    assert isinstance(res_data, list)
    assert len(res_data) == 1


@pytest.mark.asyncio
async def test_patch_dish(async_client, event_loop):
    url = f'{os.getenv("MENU_ID")}/submenus/{os.getenv("SUBMENU_ID")}/dishes/{os.getenv("DISH_ID")}'
    title = "UPDATED dish 1"
    description = "UPDATED dish description 1"
    price = "321.244"
    data = {
        "title": title,
        "description": description,
        "price": price,
    }
    response = await async_client.patch(f"/api/v1/menus/{url}", json=data)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data.get("title") == title
    assert res_data.get("description") == description
    assert res_data.get("price") == "321.24"

    url = os.getenv("MENU_ID")[:-1] + "0"
    response = await async_client.get(f"/api/v1/menus/{url}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}
