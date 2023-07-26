# fastapi-poetry-demo

## 技术栈

- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tortoise ORM](https://tortoise.github.io/)

## 初始化项目，下载依赖项

```bash
poetry install
```

## 导出依赖项配置到requirements.txt

```bash
poetry export --output requirements.txt
```

不导出Hash：

```bash
poetry export -f requirements.txt --output requirements-prod.txt --without-hashes
```

## 运行服务

```bash
poetry run python app/base.py
```

## 运行测试

```bash
pytest tests/unit -v -s
```

## 访问API文档 Swagger UI

<http://127.0.0.1:8000/docs>
