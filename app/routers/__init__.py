from . import root
from . import demo
from . import user


# 导入所有路由
def include_router(app):
    app.include_router(root.router, tags=["根服务"])
    app.include_router(demo.router, tags=["demo服务"])
    app.include_router(user.router, tags=["账号服务"])
