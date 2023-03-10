from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class MainSubmenu(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    title: str | None = "Submenu title"
    description: str | None = "Submenu description"
    dishes_count: int = 0


class SubmenuIn(BaseModel):
    title: str | None = "Submenu title"
    description: str | None = "Submenu description"


class SubmenuUpdate(BaseModel):
    title: str | None = "Update Submenu title"
    description: str | None = "Update Submenu description"
