from sqlalchemy import Table, Column, String, ForeignKey, NUMERIC
from sqlalchemy.dialects.postgresql import UUID
from .base import metadate
import uuid

menu = Table(
    "menu",
    metadate,
    Column("id", UUID, primary_key=True, default=uuid.uuid4),
    Column("title", String),
    Column("description", String)
)

submenu = Table(
    "submenu",
    metadate,
    Column("id", UUID, primary_key=True, default=uuid.uuid4),
    Column("title", String),
    Column("description", String),
    Column("menu_id", ForeignKey("menu.id", ondelete="CASCADE"),
           nullable=False)
)

dish = Table(
    "dish",
    metadate,
    Column("id", UUID, primary_key=True, default=uuid.uuid4),
    Column("title", String),
    Column("description", String),
    Column("price", NUMERIC(precision=10, scale=2)),
    Column("submenu_id", ForeignKey("submenu.id", ondelete="CASCADE"),
           nullable=False)
)
