from uuid import uuid4

from pydantic import UUID4, BaseModel, Field, root_validator


class BaseDish(BaseModel):
    class Config:
        validator_assigment = True

    @root_validator
    def set_correct_price(cls, values):
        values['price'] = '%.2f' % float(values.get('price'))
        return values


class MainDish(BaseDish):
    id: UUID4 = Field(default_factory=uuid4)
    title: str | None = 'Dish title'
    description: str | None = 'Dish description'
    price: str | None = '13.424'


class DishIn(BaseDish):
    title: str | None = 'Dish title'
    description: str | None = 'Dish description'
    price: str | None = '13.424'


class DishUpdate(BaseDish):
    title: str | None = 'Update Dish title'
    description: str | None = 'Update Dish description'
    price: str | None = '55.5232'
