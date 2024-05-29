from . import root
from . import user
from . import authn


# 导入所有路由
def include_router(app):
    app.include_router(root.router, tags=["根服务"])
    app.include_router(user.router, tags=["账号服务"])
    app.include_router(authn.router, tags=["认证服务"])
