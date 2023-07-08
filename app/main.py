from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import settings
from .routers.bot import bot
from .routers.typingsvg import typing_svg

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=settings.STATIC_DIRECTORY), name="static")
app.include_router(typing_svg.router)
app.include_router(bot.router)


@app.get("/")
async def root():
    return {"message": "GitHub Api"}
