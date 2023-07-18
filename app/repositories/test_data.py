import json

from db.tables import Dish, Menu, Submenu


class TestDataRepository:
    async def create(self, session):
        with open("test_data.json", encoding="utf-8") as file:
            content = file.read()

        data = json.loads(content)

        for menu in data:
            await self.create_record(
                session,
                menu["title"],
                menu["description"],
                m_id=menu["id"],
            )
            for submenu in menu["submenus"]:
                await self.create_record(
                    session,
                    submenu["title"],
                    submenu["description"],
                    menu_id=submenu["menu_id"],
                    sm_id=submenu["id"],
                )
                for dish in submenu["dishes"]:
                    await self.create_record(
                        session,
                        dish["title"],
                        dish["description"],
                        price=dish["price"],
                        submenu_id=dish["submenu_id"],
                        d_id=dish["id"],
                    )

        return {"status": True, "message": "Test data has been created"}

    @staticmethod
    async def create_record(
        session,
        title: str,
        description: str,
        price: str | None = None,
        m_id: str | None = None,
        sm_id: str | None = None,
        d_id: str | None = None,
        menu_id: str | None = None,
        submenu_id: str | None = None,
    ) -> None:
        if submenu_id:
            record = Dish(
                id=d_id,
                title=title,
                description=description,
                price=price,
                submenu_id=submenu_id,
            )
        elif menu_id:
            record = Submenu(
                id=sm_id,
                title=title,
                description=description,
                menu_id=menu_id,
            )
        else:
            record = Menu(
                id=m_id,
                title=title,
                description=description,
            )

        session.add(record)
        await session.flush()
