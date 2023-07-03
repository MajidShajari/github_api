from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from ..core.config import settings

templates = Jinja2Templates(directory=settings.TEMPLETE_DIRECTORY)
router = APIRouter(prefix="/typingsvg", tags=["Typing SVG"])


@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("/demo/index.html", {"request": request})
