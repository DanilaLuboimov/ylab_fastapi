import pytest
import os
from db.base import database
from sqlalchemy import text


@pytest.mark.asyncio
async def test_create_dish(async_client, event_loop, create_dish):
    title = "TEST dish 1"
    description = "TEST dish description 1"
    data = {
        "title": title,
        "description": description,
        "price": "13"
    }
    url = f'{os.getenv("MENU_ID")}/submenus/{os.getenv("SUBMENU_ID")}/dishes/'
    response = await async_client.post(f"/api/v1/menus/{url}", json=data)
    assert response.status_code == 201
    res_data = response.json()
    assert res_data.get("title") == title
    assert res_data.get("description") == description
    assert res_data.get("price") == "13"
    query = text(f"""
        DELETE FROM dish WHERE id = '{res_data.get('id')}'
    """)
    await database.execute(query)


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
    price = "321.000"
    data = {
        "title": title,
        "description": description,
        "price": price
    }
    response = await async_client.patch(f"/api/v1/menus/{url}", json=data)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data.get("title") == title
    assert res_data.get("description") == description
    assert res_data.get("price") == "321.00"

    url = os.getenv("MENU_ID")[:-1] + "0"
    response = await async_client.get(f"/api/v1/menus/{url}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}