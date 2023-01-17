from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, UUID4, Field


class Submenu(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    title: Optional[str] = None
    description: Optional[str] = None
    dishes_count: int = 0


class SubmenuIn(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
