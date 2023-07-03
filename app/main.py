from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .core.config import settings
from .routers import typing_svg

app = FastAPI()

app.mount("/static", StaticFiles(directory=settings.STATIC_DIRECTORY), name="static")
app.include_router(typing_svg.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
