from . import root
from . import demo
from . import user


# 导入所有路由
def include_router(app):
    app.include_router(root.router)
    app.include_router(demo.router)
    app.include_router(user.router)
