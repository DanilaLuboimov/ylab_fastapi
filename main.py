import uvicorn
from fastapi import FastAPI

from db.base import async_session, engine
from db.tables import Base
from endpoints import dish, menu, submenu

app = FastAPI(title='Restaurant menu')
app.include_router(menu.router, prefix='/api/v1/menus', tags=['menus'])
app.include_router(submenu.router, prefix='/api/v1/menus', tags=['submenus'])
app.include_router(dish.router, prefix='/api/v1/menus', tags=['dishes'])


@app.on_event('startup')
async def startup():
    async with async_session():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
