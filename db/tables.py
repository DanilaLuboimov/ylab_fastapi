import uuid

from sqlalchemy import NUMERIC, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    menu_id = Column(
        ForeignKey('menu.id', ondelete='CASCADE'),
        nullable=False, )


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    price = Column(NUMERIC(precision=10, scale=2))
    submenu_id = Column(
        ForeignKey('submenu.id', ondelete='CASCADE'),
        nullable=False, )
