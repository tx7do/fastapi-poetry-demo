from fastapi import FastAPI
import uvicorn
import redis.asyncio as redis

from starlette.middleware.cors import CORSMiddleware

from tortoise.contrib.fastapi import register_tortoise

from app import settings
from app.routers import include_router


# 初始化服务端应用
def create_app():
    # 创建fastapi
    _app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION
    )

    # 添加CORS中间件
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # 导入路由
    include_router(_app)

    # 注册Tortoise ORM
    register_tortoise(
        _app,
        config={
            "connections": {"default": settings.DATABASE_DSN},
            "apps": {
                "models": {
                    "models": ["app.models"],
                    "default_connection": "default",
                }
            },
        },
        generate_schemas=True,
    )

    return _app


app = create_app()

# 运行FastAPI应用
if __name__ == "__main__":
    uvicorn.run(
        app='main:app',
        host="0.0.0.0", port=settings.SERVER_PORT,
        reload=True
    )
