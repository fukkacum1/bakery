import asyncio
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.future import select

from app.schemas import ProductFilter, ProductCreate, ProductStructureCreate
from app.db.dao import ProductDao, BakeryDao, IngredientDao, ProductStructureDao
from app.db.models import Product, Bakery, Ingredient, ProductStructure
from app.db.session_maker import db

router = APIRouter()

def get_dao(db_session: AsyncSession = Depends(db.get_db)) -> ProductDao:
    return ProductDao(db_session)

@router.post(
    path="/bakery/{bakery_id}/add_product",
    summary="Добавление изделия в хлебозавод по ID",
    responses={
        200: {"description": "Изделие успешно добавлено"},
        400: {"description": "Некорректные данные"},
        404: {"description": "Хлебозавод или ингредиенты не найдены"},
        500: {"description": "Ошибка сервера"}
    }
)
async def add_product_by_bakery_id(
        bakery_id: int = Path(..., description="ID хлебозавода"),
        product_data: ProductCreate = Body(),
        db: AsyncSession = Depends(db.get_db_with_commit)
) -> JSONResponse:
    try:
        bakery = await BakeryDao(db).find_one_or_none_by_id(bakery_id)
        if not bakery:
            raise HTTPException(status_code=404, detail=f"Хлебозавод с ID {bakery_id} не найден")

        ingredients = []
        for ingredient_id in product_data.ingredients:
            ingredient = await IngredientDao(db).find_one_or_none_by_id(ingredient_id)
            ingredients.append(ingredient)


        if len(ingredients) != len(product_data.ingredients):
            raise HTTPException(status_code=404, detail="Некоторые из указанных ингредиентов не найдены")

        product_data.bakery_id = bakery_id
        new_product = await ProductDao(db).add(values=ProductCreate(**product_data.model_dump(exclude={"ingredients"})))

        if not new_product:
            raise HTTPException(status_code=500, detail="Не удалось получить идентификатор изделия")

        new_product_id = new_product.get("id")

        product_structures = [
            ProductStructureCreate(product_id=new_product_id, ingredient_id=ingredient_id)
            for ingredient_id in product_data.ingredients
        ]
        await ProductStructureDao(db).add_many(product_structures)


        return JSONResponse(status_code=200, content={"message": "Изделие вместе с составом успешно добавлено"})


    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении изделия в хлебозавод {bakery_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка базы данных")
    except Exception as e:
        logger.error(f"Ошибка при добавлении изделия в хлебозавод {bakery_id}: {e}")
        raise HTTPException(status_code=500, detail="Неизвестная ошибка сервера")


@router.delete(
    path="/bakery/{bakery_id}/product/{product_id}/delete",
    summary="Удаление изделия по ID из хлебозавода по ID",
    responses={
        200: {"description": "Изделие успешно удалено"},
        404: {"description": "Изделие или хлебозавод не найдены"},
        500: {"description": "Ошибка сервера"}
    }
)
async def delete_product_by_bakery_and_product_id(
        bakery_id: int = Path(..., description="ID хлебозавода"),
        product_id: int = Path(..., description="ID изделия"),
        db: AsyncSession = Depends(db.get_db_with_commit)
) -> JSONResponse:
    try:
        bakery = await BakeryDao(db).find_one_or_none_by_id(bakery_id)
        if not bakery:
            raise HTTPException(status_code=404, detail=f"Хлебозавод с ID {bakery_id} не найден")

        product = await ProductDao(db).find_one_or_none_by_id(product_id)
        if not product or product.bakery_id != bakery_id:
            raise HTTPException(
                status_code=404,
                detail=f"Изделие с ID {product_id} не найдено для хлебозавода с ID {bakery_id}"
            )

        success = await ProductDao(db).delete_by_id(product_id)
        if success:
            return JSONResponse(
                status_code=200,
                content={"message": f"Изделие с ID {product_id} успешно удалено из хлебозавода с ID {bakery_id}"}
            )
        else:
            raise HTTPException(status_code=404, detail=f"Изделие с ID {product_id} не найдено")

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении изделия {product_id} из хлебозавода {bakery_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка базы данных")
    except Exception as e:
        logger.error(f"Ошибка при удалении изделия {product_id} из хлебозавода {bakery_id}: {e}")
        raise HTTPException(status_code=500, detail="Неизвестная ошибка сервера")

@router.get(
    path="/all_products",
    summary="Получение всех изделий",
    responses={
        200: {"description": "Изделия успешно получены"},
        404: {"description": "Изделия не найдены"}
    }
)
async def get_all_products(
        db: AsyncSession = Depends(db.get_db)
):
    products_data: List[Product] = await ProductDao(db).find_all()

    if not products_data:
        raise HTTPException(status_code=404, detail="Изделия не найдены")

    # for product in products_data:
    #     product = product.to_dict()

    return JSONResponse(status_code=200, content=[product.to_dict() for product in products_data])


@router.get(
    path="/bakery/{bakery_id}/products",
    summary="Получение всех изделий хлебозавода по ID",
    responses={
        200: {"description": "Изделия успешно получены"},
        404: {"description": "Изделия не найдены для данного хлебозавода"}
    }
)
async def get_products_by_bakery_id(
    bakery_id: int = Path(..., description="ID хлебозавода"),
    db: AsyncSession = Depends(db.get_db)
):
    products_data: List[Product] = await ProductDao(db).find_all(filters=ProductFilter(bakery_id=bakery_id))

    if not products_data:
        raise HTTPException(status_code=404, detail=f"Изделия для хлебозавода с id={bakery_id} не найдены")

    return JSONResponse(status_code=200, content=[product.to_dict() for product in products_data])

@router.get(
    path="/{product_id}",
    summary="Получение изделия по ID",
    responses={
        200: {"description": "Изделие успешно получено"},
        404: {"description": "Изделие не найдено"}
    }
)
async def get_product_by_id(product_id: int = Path(..., description="ID изделия"),
    db: AsyncSession = Depends(db.get_db)
):
    product: Product | None = await ProductDao(db).find_one_or_none_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Изделие с id={product_id} не найдено")

    return JSONResponse(status_code=200, content=product.to_dict())

@router.get(
    path="/bakery/{bakery_id}/products/total_price",
    summary="Получение суммарной стоимости всех изделий хлебозавода по ID",
    responses={
        200: {"description": "Суммарная стоимость изделий успешно получена"},
        404: {"description": "Изделия не найдены для данного хлебозавода"}
    }
)
async def get_total_price_by_bakeries_id(
    bakery_id: int = Path(..., description="ID хлебозавода"),
    db: AsyncSession = Depends(db.get_db)
):
    try:
        total_price = await ProductDao(db).products_total_price_by_bakery_id(ProductFilter(bakery_id=bakery_id))

        if total_price == 0.0:
            raise HTTPException(status_code=404, detail=f"Изделия для хлебозавода с id={bakery_id} не найдены")

        return {"total_price": total_price}
    except Exception as e:
        logger.error(f"Ошибка при подсчёте стоимости продуктов для хлебозавода {bakery_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get(
    path="/bakery/{bakery_id}/products/total_price",
    summary="Получение суммарной стоимости всех изделий хлебозавода по ID",
    responses={
        200: {"description": "Суммарная стоимость изделий успешно получена"},
        404: {"description": "Изделия не найдены для данного хлебозавода"}
    }
)
async def get_total_price_by_bakeries_id(
    bakery_id: int = Path(..., description="ID хлебозавода"),
    db: AsyncSession = Depends(db.get_db)
):
    try:
        products_data: List[Product] = await ProductDao(db).find_all(filters=ProductFilter(bakery_id=bakery_id))

        if not products_data:
            raise HTTPException(status_code=404, detail=f"Изделия для хлебозавода с id={bakery_id} не найдены")

        total_price = float(sum(product.price for product in products_data))

        return JSONResponse(status_code=200, content={"total_price": total_price})
    except Exception as e:
        logger.error(e)


@router.get(
    path="/products/max_profit",
    summary="Нахождение изделия с максимальной прибылью",
    responses={
        200: {"description": "Наиболее прибыльное изделие успешно найдено"},
        404: {"description": "Не найдено ни одно изделие"}
    }
)
async def get_most_profitable_product(
        db: AsyncSession = Depends(db.get_db)
):
    try:
        most_profitable = await ProductDao(db).find_most_profitable_product()

        if not most_profitable:
            raise HTTPException(status_code=404, detail="Не найдено ни одно изделие")

        return JSONResponse(status_code=200, content=most_profitable)

    except Exception as e:
        logger.error(f"Ошибка при получении наиболее прибыльного изделия: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get(
    path="/products/invalid",
    summary="Поиск изделий, нарушающих срок годности ингредиентов",
    responses={
        200: {"description": "Список изделий, нарушивших срок годности ингредиентов"},
        404: {"description": "Нарушений не найдено"}
    }
)

async def get_invalid_products(
        dao: ProductDao = Depends(get_dao)):
    try:
        invalid_products = await dao.find_invalid_products()
        if not invalid_products:
            raise HTTPException(status_code=404, detail="Нарушений не найдено")
        return invalid_products
    except Exception as e:
        logger.error(f"Ошибка при проверке изделий на соответствие: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")