from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import settings
from .routers import typing_svg

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=settings.STATIC_DIRECTORY), name="static")
app.include_router(typing_svg.router)


@app.post("/shijarbot")
async def root(request: Request):
    response = await request.json()
    print(response["message"]["text"])
