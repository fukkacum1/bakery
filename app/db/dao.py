from decimal import Decimal

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func, desc, Integer, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.base import BaseDAO
from app.db.models import Bakery, Product, Ingredient, ProductStructure
from app.schemas import ProductFilter, ProductStructureFilter

from loguru import logger


class BakeryDao(BaseDAO[Bakery]):
    model = Bakery

    async def get_sorted_bakeries_by_production_volume(self):
        try:
            query = (
                select(
                    Bakery.name.label("bakery_name"),
                    func.sum(Product.production_volume).label("total_production_volume")
                )
                .join(Product, Product.bakery_id == Bakery.id)
                .group_by(Bakery.id)
                .order_by(desc(func.sum(Product.production_volume)))
            )

            result = await self._session.execute(query)
            sorted_bakeries = result.fetchall()

            return sorted_bakeries
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при сортировке хлебозаводов: {e}")
            raise


class ProductDao(BaseDAO[Product]):
    model = Product

    async def products_total_price_by_bakery_id(self, filters: ProductFilter):
        try:
            bakery_id = filters.bakery_id
            logger.info(f"Суммарная стоимость всех изделий, выпускаемых хлебозаводом с ID: {bakery_id}")
            query = (
                select(func.sum(func.coalesce(self.model.price, 0) * func.coalesce(self.model.production_volume, 0)))
                .where(self.model.bakery_id == bakery_id)
            )

            result = await self._session.execute(query)
            total_price: Decimal = result.scalar()

            if total_price is not None:
                total_price_float = float(total_price)
                logger.info(
                    f"Суммарная стоимость изделий хлебозавода с ID: {bakery_id}: {total_price_float}")
            else:
                total_price_float = 0.0
                logger.info(f"Суммарная стоимость изделий хлебозавода с ID: {bakery_id} не найдена")

            return total_price_float
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске суммарной стоимости для хлебозавода с ID {bakery_id}: {e}")
            raise

    async def find_most_profitable_product(self):
        try:
            query = (
                select(
                    self.model.name,
                    func.coalesce(self.model.price, 0) * func.coalesce(self.model.production_volume, 0)
                )
                .order_by(func.coalesce(self.model.price, 0) * func.coalesce(self.model.production_volume, 0).desc())
                .limit(1)
            )

            result = await self._session.execute(query)
            row = result.fetchone()

            if row:
                return {"product_name": row[0], "profit": float(row[1])}
            else:
                return None

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при определении наиболее прибыльного изделия: {e}")
            raise

    async def find_invalid_products(self):
        try:
            query = (
                select(
                    Product.name.label("product_name"),
                    Ingredient.name.label("ingredient_name"),
                    Product.created_at.label("production_date"),
                    (Ingredient.date_delivery + func.cast(Ingredient.shelf_life, Integer) * text("INTERVAL '1 day'")).label("expiration_date")

                )
                .join(ProductStructure, Product.id == ProductStructure.product_id)
                .join(Ingredient, ProductStructure.ingredient_id == Ingredient.id)
                .where(
                    Product.created_at > Ingredient.date_delivery + func.cast(Ingredient.shelf_life, Integer) * text("INTERVAL '1 day'"),
                )
            )

            result = await self._session.execute(query)
            rows = result.fetchall()

            if not rows:
                return None

            return [
                {
                    "product_name": row.product_name,
                    "ingredient_name": row.ingredient_name,
                    "production_date": row.production_date.strftime('%Y-%m-%d'),
                    "expiration_date": row.expiration_date.strftime('%Y-%m-%d'),
                }
                for row in rows
            ]

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске невалидных изделий: {e}")
            raise

    async def delete_by_id(self, product_id):
        try:
            logger.info(f"Удаление изделия с ID: {product_id}")

            await self._session.execute(
                delete(ProductStructure).where(ProductStructure.product_id == product_id)
            )
            logger.info(f"Связи для изделия с ID {product_id} успешно удалены")

            query = select(self.model).where(self.model.id == product_id).limit(1)
            result = await self._session.execute(query)
            product = result.scalar_one_or_none()

            if product is None:
                logger.warning(f"Изделие с ID {product_id} не найдено")
                return False

            await self._session.delete(product)
            await self._session.commit()
            logger.info(f"Изделие с ID {product_id} успешно удалено")
            return True

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении изделия с ID {product_id}: {e}")
            await self._session.rollback()
            raise


class ProductStructureDao(BaseDAO[ProductStructure]):
    model = ProductStructure

    async def find_product_with_max_ingredients(self):
        try:
            logger.info("Поиск изделия с максимальным количеством ингредиентов")

            subquery = (
                select(
                    self.model.product_id,
                    func.count(self.model.ingredient_id).label("ingredients_count")
                )
                .group_by(self.model.product_id)
                .order_by(func.count(self.model.ingredient_id).desc())
                .limit(1)
            )

            result = await self._session.execute(subquery)
            row = result.first()

            if row is None:
                logger.info("Изделия с ингредиентами не найдены")
                return None

            product_id, ingredients_count = row
            logger.info(f"Максимальное количество ингредиентов: {ingredients_count} для продукта с ID {product_id}")

            return {"product_id": product_id, "ingredients_count": ingredients_count}

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске максимального кол-ва ингредиентов: {e}")
            raise


    async def get_product_with_ingredients(self, product_id: int):
        try:
            query = (
                select(Product.name, Ingredient.name)
                .join(ProductStructure, Product.id == ProductStructure.product_id)
                .join(Ingredient, ProductStructure.ingredient_id == Ingredient.id)
                .where(Product.id == product_id)
            )

            result = await self._session.execute(query)
            rows = result.fetchall()

            if not rows:
                return None

            product_name = rows[0][0]
            ingredients = [row[1] for row in rows]
            return {"product_name": product_name, "ingredients": ingredients}

        except SQLAlchemyError as e:
            logger.error(f"Ошибка выполнения запроса get_product_with_ingredients для продукта {product_id}: {e}")
            raise


class IngredientDao(BaseDAO[Ingredient]):
    model = Ingredient


