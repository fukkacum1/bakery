from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.db.session_maker import db
from app.db.dao import BakeryDao

router = APIRouter()

@router.get(
    "/bakeries/sorted",
    summary="Сортировка хлебозаводов по объему производства",
    operation_id="get_sorted_bakeries",
    responses={
        200: {"description": "Сортировка успешно выполнена"},
        404: {"description": "Хлебозаводы не найдены"}
    }
)
async def get_sorted_bakeries(
        db: AsyncSession = Depends(db.get_db)
):
    try:
        logger.info("Запрос на сортировку хлебозаводов начат")
        bakery_dao = BakeryDao(db)
        sorted_bakeries = await bakery_dao.get_sorted_bakeries_by_production_volume()
        logger.info(f"Найдено {len(sorted_bakeries)} хлебозаводов")
        if not sorted_bakeries:
            raise HTTPException(status_code=404, detail="Хлебозаводы не найдены")

        return [
            {
                "bakery_name": bakery.bakery_name,
                "total_production_volume": bakery.total_production_volume
            }
            for bakery in sorted_bakeries
        ]
    except Exception as e:
        logger.error(f"Ошибка в обработке запроса `/bakeries/sorted`: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при сортировке хлебозаводов")