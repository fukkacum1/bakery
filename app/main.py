from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import product, ingredient, bakery


def create_app() -> FastAPI:
    app =  FastAPI(
        title="хлебозавод"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    app.include_router(product.router, tags=["Работа с изделиями"])
    app.include_router(ingredient.router, tags=["Работа с ингредиентами"])
    app.include_router(bakery.router, tags=["Работа с хлебозаводами"])

    return app


app = create_app()

