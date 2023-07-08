from fastapi import APIRouter, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from ...core.config import settings
from .generate_svg import Svg

templates = Jinja2Templates(directory=settings.TEMPLETE_DIRECTORY)
router = APIRouter(prefix="/typingsvg", tags=["Typing SVG"])


@router.get("/")
async def root(request: Request):
    query_dict = dict(request.query_params)
    if "lines" not in query_dict:
        return templates.TemplateResponse("/typing_svg/demo.html", {"request": request})
    svg_element = Svg(query_dict)
    return Response(content=svg_element.svg_string(), media_type="image/svg+xml")
