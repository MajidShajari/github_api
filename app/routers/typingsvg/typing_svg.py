from typing import Dict

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from ...core.config import settings
from ...utils.google_font_convertor import GoogleFontConverter

templates = Jinja2Templates(directory=settings.TEMPLETE_DIRECTORY)
router = APIRouter(prefix="/typingsvg", tags=["Typing SVG"])


@router.get("/")
async def root(request: Request):
    query_dict = dict(request.query_params)
    if "lines" not in query_dict:
        return templates.TemplateResponse("/typing_svg/demo.html", {"request": request})
    google_font = GoogleFontConverter()
    return templates.TemplateResponse("/typing_svg/main.html", {"request": request})
