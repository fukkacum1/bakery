from typing import List
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from app.schemas import ProductStructureFilter
from app.db.dao import ProductStructureDao, ProductDao
from app.db.models import Ingredient, ProductStructure, Product
from app.db.session_maker import db

router = APIRouter(prefix="/ingredients")

@router.get(
    path="/all_ingredients",
    summary="Получение всех ингредиентов",
    responses={
        200: {"description": "Ингредиенты успешно получены"},
        404: {"description": "Ингредиенты не найдены"}
    }
)
async def get_all_ingredients(db: AsyncSession = Depends(db.get_db)):
    ingredients_data: List[Ingredient] = await ProductStructureDao(db).find_all()

    if not ingredients_data:
        raise HTTPException(status_code=404, detail="Ингредиенты не найдены")

    return JSONResponse(status_code=200, content=[ingredient.to_dict() for ingredient in ingredients_data])

@router.get(
    path="/{product_id}",
    summary="Получение всех ингредиентов по ID продукта",
    responses={
        200: {"description": "Ингредиенты продукта успешно получены"},
        404: {"description": "Ингредиенты не найдены"}
    }
)
async def get_ingredients_by_id_product(
        product_id: int = Path(..., description="ID продукта"),
        db: AsyncSession = Depends(db.get_db)
):
    try:
        product_with_ingredients = await ProductStructureDao(db).get_product_with_ingredients(product_id)

        if not product_with_ingredients:
            raise HTTPException(status_code=404, detail=f"Ингредиенты для продукта с id={product_id} не найдены")

        return JSONResponse(status_code=200, content=product_with_ingredients)

    except Exception as e:
        logger.error(f"Ошибка при получении ингредиентов для продукта с id={product_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get(
    path="/products/max_count_ingredients",
    summary="Получение изделия с максимальным количеством ингредиентов",
    responses={
        200: {"description": "Изделие с максимальным количеством ингредиентов найдено"},
        404: {"description": "Изделие не найдено"}
    },
    response_model=None
)
async def get_product_with_max_ingredients(
        db: AsyncSession = Depends(db.get_db),
):
    try:
        result = await ProductStructureDao(db).find_product_with_max_ingredients()
        if result is None:
            raise HTTPException(status_code=404, detail="Изделия с ингредиентами не найдены")

        product = await ProductDao(db).find_one_or_none_by_id(result.get("product_id"))

        if not product:
            raise HTTPException(status_code=404, detail="Изделие не найдено")

        return {
            "product": product,
            "ingredients_count": result["ingredients_count"],
        }
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при поиске изделия с максимальным количеством ингредиентов: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")