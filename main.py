import uvicorn
from fastapi import FastAPI
from db.base import database
from endpoints import menu, submenu, dish

app = FastAPI(title="Restaurant menu")
app.include_router(menu.router, prefix="/api/v1/menus", tags=["menus"])
app.include_router(submenu.router, prefix="/api/v1/menus", tags=["submenus"])
app.include_router(dish.router, prefix="/api/v1/menus", tags=["dishes"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
