from fastapi import FastAPI

app = FastAPI(title='CMS', description='simple cms')


@app.get("/", summary='根接口', description='根接口描述', tags=['根节点'])
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# 运行FastAPI应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True)
