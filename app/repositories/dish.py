from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import Dish
from models.dish import DishIn, DishUpdate, MainDish


class DishRepository:
    @staticmethod
    async def get_all(session: AsyncSession, sm_id: str) -> list:
        stmt = select(
            Dish.id,
            Dish.title,
            Dish.description,
            Dish.price,
        ).where(
            Dish.submenu_id == sm_id,
        )

        result = await session.execute(stmt)

        answer = result.all()
        return answer

    @staticmethod
    async def create(
        session: AsyncSession,
        sm_id: str,
        d: DishIn,
    ) -> MainDish:
        new_record = MainDish(
            title=d.title,
            description=d.description,
            price=d.price,
        )

        new_dish = Dish(
            id=new_record.id,
            title=new_record.title,
            description=new_record.description,
            price=new_record.price,
            submenu_id=sm_id,
        )

        session.add(new_dish)
        await session.flush()
        return new_record

    @staticmethod
    async def patch(
        session: AsyncSession,
        d_id: str,
        d: DishUpdate,
    ) -> None:
        stmt = (
            update(
                Dish,
            )
            .where(
                Dish.id == d_id,
            )
            .values(
                **d.dict(),
            )
        )

        await session.execute(stmt)

    @staticmethod
    async def delete(
        session: AsyncSession,
        record,
    ) -> dict:
        await session.delete(record)
        return {"status": True, "message": "The dish has been deleted"}

    @staticmethod
    async def get_by_id(
        session: AsyncSession, d_id: str
    ) -> tuple[MainDish | None, dict | None]:
        stmt = select(
            Dish.id,
            Dish.title,
            Dish.description,
            Dish.price,
        ).where(
            Dish.id == d_id,
        )

        result = await session.execute(stmt)

        record = result.one_or_none()

        if record is None:
            return None, None

        cache_dict = MainDish.parse_obj(record).dict()
        return record, cache_dict

    @staticmethod
    async def check_by_id(
        session: AsyncSession,
        d_id: str,
    ) -> Dish:
        stmt = select(
            Dish,
        ).where(
            Dish.id == d_id,
        )

        result = await session.scalar(stmt)
        return result
