from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey,Table, Column

from app.models.base import Base
from app.models.ingredient import Ingredient
from app.models.associate import pizza_ingred_assoc_table


class Pizza(Base):
    __tablename__ = "pizzas"

    id: Mapped[int] = mapped_column("id", primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column()
    ingredients: Mapped[List[Ingredient]] = relationship(secondary=pizza_ingred_assoc_table)


assoc_pizza = Table(
    "assoc_pizza",
    Base.metadata,
    Column("name_id", ForeignKey("pizzalist.id")),
    Column("pizzas_id", ForeignKey("pizzas.id"))
)

class MenuList(Base):
    __tablename__ = "pizzalist"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    pizzas: Mapped[List[Pizza]] = relationship(secondary=assoc_pizza)


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    grade: Mapped[int] = mapped_column()


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    grade_id: Mapped[int] = mapped_column(ForeignKey(Grade.id))
    text: Mapped[str] = mapped_column(String())
    grade: Mapped[Grade] = relationship()