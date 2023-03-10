import os

import pytest
from sqlalchemy import delete

from db.tables import Menu


@pytest.mark.asyncio
async def test_create_menu(async_client, async_session, event_loop):
    title = "random TEST menu 1"
    description = "random TEST menu description 1"
    data = {
        "title": title,
        "description": description,
    }
    response = await async_client.post("/api/v1/menus/", json=data)
    assert response.status_code == 201
    res_data = response.json()
    assert res_data.get("title") == title
    assert res_data.get("description") == description
    assert res_data.get("submenus_count") == 0
    assert res_data.get("dishes_count") == 0

    stmt = delete(Menu).where(Menu.id == res_data.get("id"))

    async with async_session.begin():
        await async_session.execute(stmt)


@pytest.mark.asyncio
async def test_get_one_menu(async_client, event_loop):
    url = os.getenv("MENU_ID")
    response = await async_client.get(f"/api/v1/menus/{url}")
    assert response.status_code == 200
    res_data = response.json()
    assert res_data.get("title") == "TEST menu 1"
    assert res_data.get("description") == "TEST menu description 1"
    assert res_data.get("submenus_count") == 1
    assert res_data.get("dishes_count") == 1

    url = os.getenv("MENU_ID")[:-1] + "0"
    response = await async_client.get(f"/api/v1/menus/{url}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}


@pytest.mark.asyncio
async def test_get_all_menus(async_client, event_loop):
    response = await async_client.get("/api/v1/menus/")
    assert response.status_code == 200
    res_data = response.json()
    assert isinstance(res_data, list)
    assert len(res_data) == 1


@pytest.mark.asyncio
async def test_patch_menu(async_client, event_loop):
    url = os.getenv("MENU_ID")
    title = "UPDATED menu 1"
    description = "UPDATED menu description 1"
    data = {
        "title": title,
        "description": description,
    }
    response = await async_client.patch(f"/api/v1/menus/{url}", json=data)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data.get("title") == title
    assert res_data.get("description") == description

    url = os.getenv("MENU_ID")[:-1] + "0"
    response = await async_client.get(f"/api/v1/menus/{url}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}
