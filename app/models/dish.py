from typing import Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field, root_validator, validator


class BaseDish(BaseModel):
    price: str

    class Config:
        validator_assigment = True

    @validator("price")
    def check_price(cls, price):
        if float(price) <= 0:
            raise ValueError("Цена за блюдо должна быть больше 0")
        return price

    @root_validator
    def set_correct_price(cls, values):
        values["price"] = "%.2f" % float(values.get("price"))
        return values


class MainDish(BaseDish):
    id: UUID4 = Field(default_factory=uuid4)
    title: str | None = "Dish title"
    description: str | None = "Dish description"
    price: str | None = "13.424"


class DishIn(BaseDish):
    title: str | None = "Dish title"
    description: str | None = "Dish description"
    price: str | None = "13.424"


class DishUpdate(BaseDish):
    title: str | None = "Update Dish title"
    description: str | None = "Update Dish description"
    price: str | None = "55.5232"
