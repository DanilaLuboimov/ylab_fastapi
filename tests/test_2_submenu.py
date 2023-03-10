import os

import pytest
from sqlalchemy import delete

from db.tables import Submenu


@pytest.mark.asyncio
async def test_create_submenu(async_client, async_session, event_loop):
    title = "TEST submenu 1"
    description = "TEST submenu description 1"
    data = {
        "title": title,
        "description": description,
        "menu_id": os.getenv("MENU_ID"),
    }
    url = f'{os.getenv("MENU_ID")}/submenus/'
    response = await async_client.post(f"/api/v1/menus/{url}", json=data)
    assert response.status_code == 201
    res_data = response.json()
    assert res_data.get("title") == title
    assert res_data.get("description") == description
    assert res_data.get("dishes_count") == 0

    stmt = delete(Submenu).where(Submenu.id == res_data.get("id"))

    async with async_session.begin():
        await async_session.execute(stmt)


@pytest.mark.asyncio
async def test_get_one_submenu(async_client, event_loop):
    url = f'{os.getenv("MENU_ID")}/submenus/{os.getenv("SUBMENU_ID")}'
    response = await async_client.get(f"/api/v1/menus/{url}")
    assert response.status_code == 200
    res_data = response.json()
    assert res_data.get("title") == "TEST submenu 1"
    assert res_data.get("description") == "TEST submenu description 1"
    assert res_data.get("dishes_count") == 1

    url = url[:-1] + "0"
    response = await async_client.get(f"/api/v1/menus/{url}")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


@pytest.mark.asyncio
async def test_get_all_submenus(async_client, event_loop):
    url = f'{os.getenv("MENU_ID")}/submenus/'
    response = await async_client.get(f"/api/v1/menus/{url}")
    assert response.status_code == 200
    res_data = response.json()
    assert isinstance(res_data, list)
    assert len(res_data) == 1


@pytest.mark.asyncio
async def test_patch_submenu(async_client, event_loop):
    url = f'{os.getenv("MENU_ID")}/submenus/{os.getenv("SUBMENU_ID")}'
    title = "UPDATED submenu 1"
    description = "UPDATED submenu description 1"
    data = {
        "title": title,
        "description": description,
    }
    response = await async_client.patch(f"/api/v1/menus/{url}", json=data)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data.get("title") == title
    assert res_data.get("description") == description
    url = url[:-1] + "0"
    response = await async_client.get(f"/api/v1/menus/{url}")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}
