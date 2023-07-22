from . import root
from . import demo


# 导入所有路由
def include_router(app):
    app.include_router(root.router)
    app.include_router(demo.router)
