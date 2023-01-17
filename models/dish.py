from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, UUID4, Field


class Dish(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None


class DishIn(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None
