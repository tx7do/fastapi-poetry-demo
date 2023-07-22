# fastapi-poetry-demo

initial requirements

```bash
poetry install
```

export config to requirements.txt

```bash
poetry export --output requirements.txt

poetry export -f requirements.txt --output requirements-prod.txt --without-hashes
```

run server app

```bash
poetry run python fastapi_poetry_demo/main.py
```

access Swagger UI:

<http://127.0.0.1:8000/docs>
