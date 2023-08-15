# fastapi-poetry-demo

## 技术栈

- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tortoise ORM](https://tortoise.github.io/)

## 运行时环境需求

- Ubuntu 22.04 LTS
- Python 3.9+

## 安装Poetry

通过安装脚本进行安装（可以保证安装到最新的版本）：

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

将配置添加到`.bashrc`：

```bash
export PATH="/home/ubuntu/.local/bin:$PATH"
```

## 初始化项目，下载依赖项

```bash
poetry install
```

## 导出依赖项配置到requirements.txt

```bash
poetry export --output config/requirements.txt
```

不导出Hash：

```bash
poetry export -f requirements.txt --output config/requirements-prod.txt --without-hashes
```

## 运行服务

```bash
poetry run python3 app/main.py
```

## 运行测试

测试全部用例：

```bash
pytest
```

测试API：

```bash
pytest tests/api -v -s
```

测试数据库增删改查：

```bash
pytest tests/crud -v -s
```

## 访问API文档

- Swagger：<http://127.0.0.1:8000/docs>
- Redoc：<http://127.0.0.1:8000/redoc>
