from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, UUID4, Field


class Menu(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    title: Optional[str] = None
    description: Optional[str] = None
    submenus_count: int = 0
    dishes_count: int = 0


class MenuIn(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
