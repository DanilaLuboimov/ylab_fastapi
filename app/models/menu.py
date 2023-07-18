from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class MainMenu(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    title: str | None = "Menu title"
    description: str | None = "Menu description"
    submenus_count: int = 0
    dishes_count: int = 0


class MenuIn(BaseModel):
    title: str | None = "Menu title"
    description: str | None = "Menu description"


class MenuUpdate(BaseModel):
    title: str | None = "Update Menu title"
    description: str | None = "Update Menu description"
