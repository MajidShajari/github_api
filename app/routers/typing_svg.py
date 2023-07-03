from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from ..core.config import settings

templates = Jinja2Templates(directory=settings.TEMPLETE_DIRECTORY)
router = APIRouter(prefix="/typingsvg", tags=["Typing SVG"])


@router.get("/")
async def root(request: Request):
    query_dict = dict(request.query_params)
    if query_dict:
        if "lines" not in query_dict:
            return {"error": "lines not exist"}
        return {"message": request.query_params}
    return templates.TemplateResponse("/typing_svg/demo.html", {"request": request})
