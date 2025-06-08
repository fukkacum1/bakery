from typing import Optional, List

from pydantic import BaseModel, Field


class TotalPrice(BaseModel):
    price: float

class ProductFilter(BaseModel):
    bakery_id: int

class ProductStructureFilter(BaseModel):
    product_id: int

class ProductCreate(BaseModel):
    name: str
    weight: float
    shelf_life: int
    production_volume: Optional[int] = None
    price: float
    bakery_id: int | None = Field(None)
    ingredients: List[int] | None = Field(None)


class ProductStructureCreate(BaseModel):
    product_id: int
    ingredient_id: int


