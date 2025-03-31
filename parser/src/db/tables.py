from database import Base
from sqlalchemy.orm import Mapped


class Ozon(Base):
    __tablename__ = "ozon_products"

    name: Mapped[str]
    link: Mapped[str]
    price: Mapped[str]
    old_price: Mapped[str]
    remaining: Mapped[str]


class Wb(Base):
    __tablename__ = "wb_products"

    name: Mapped[str]
    link: Mapped[str]
    price: Mapped[str]
    old_price: Mapped[str]


class Auchan(Base):
    __tablename__ = "auchan_products"

    name: Mapped[str]
    link: Mapped[str]
    price: Mapped[str]
    old_price: Mapped[str]
