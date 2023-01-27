import os

import pytest


@pytest.mark.asyncio
async def test_delete_dish(async_client, event_loop):
    url = f'{os.getenv("MENU_ID")}/submenus/{os.getenv("SUBMENU_ID")}/dishes/{os.getenv("DISH_ID")}'
    response = await async_client.delete(f'/api/v1/menus/{url}')
    assert response.status_code == 200
    assert response.json() == {
        'status': True,
        'message': 'The dish has been deleted',
    }


@pytest.mark.asyncio
async def test_delete_submenu(async_client, event_loop):
    url = f'{os.getenv("MENU_ID")}/submenus/{os.getenv("SUBMENU_ID")}'
    response = await async_client.delete(f'/api/v1/menus/{url}')
    assert response.status_code == 200
    assert response.json() == {
        'status': True,
        'message': 'The submenu has been deleted',
    }


@pytest.mark.asyncio
async def test_delete_menu(async_client, event_loop):
    url = os.getenv('MENU_ID')
    response = await async_client.delete(f'/api/v1/menus/{url}')
    assert response.status_code == 200
    assert response.json() == {
        'status': True,
        'message': 'The menu has been deleted',
    }
