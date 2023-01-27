from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class Dish(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    title: str | None = 'Dish title'
    description: str | None = 'Dish description'
    price: str | None = '13.424'


class DishIn(BaseModel):
    title: str | None = 'Dish title'
    description: str | None = 'Dish description'
    price: str | None = '13.424'
