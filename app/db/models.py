from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, Numeric, ForeignKey
from datetime import date
from typing import List
from app.db.database import Base


class Bakery(Base):
    __tablename__ = "bakeries"

    id = mapped_column(Integer, autoincrement=True, primary_key=True)


    name: Mapped[str] = mapped_column(String(255), nullable=False)
    production_date: Mapped[date] = mapped_column(Date, nullable=False)

    products: Mapped[List["Product"]] = relationship("Product", back_populates="bakery")

    def __repr__(self):
        return f"<Bakery(name={self.name}, production_date={self.production_date})>"


class Product(Base):
    __tablename__ = "products"

    id = mapped_column(Integer, autoincrement=True, primary_key=True)


    name: Mapped[str] = mapped_column(String(255), nullable=False)
    weight: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    shelf_life: Mapped[int] = mapped_column(Integer, nullable=False)
    production_volume: Mapped[int] = mapped_column(Integer, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    bakery_id: Mapped[int] = mapped_column(Integer, ForeignKey("bakeries.id"), nullable=False)

    bakery: Mapped["Bakery"] = relationship("Bakery", back_populates="products")
    product_structures: Mapped[List["ProductStructure"]] = relationship("ProductStructure", back_populates="product")

    def __repr__(self):
        return f"<Product(name={self.name}, bakery_id={self.bakery_id})>"


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = mapped_column(Integer, autoincrement=True, primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    weight_ingredient: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    date_delivery: Mapped[date] = mapped_column(Date, nullable=False)
    shelf_life: Mapped[int] = mapped_column(Integer, nullable=False)

    product_structures: Mapped[List["ProductStructure"]] = relationship("ProductStructure", back_populates="ingredient")

    def __repr__(self):
        return f"<Ingredient(name={self.name})>"


class ProductStructure(Base):
    __tablename__ = "product_structures"

    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(Integer, ForeignKey("ingredients.id"), primary_key=True)

    product: Mapped["Product"] = relationship("Product", back_populates="product_structures")
    ingredient: Mapped["Ingredient"] = relationship("Ingredient", back_populates="product_structures")

    def __repr__(self):
        return f"<ProductStructure(product_id={self.product_id}, ingredient_id={self.ingredient_id})>"
