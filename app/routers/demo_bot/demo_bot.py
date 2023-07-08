from fastapi import APIRouter, Request

router = APIRouter(prefix="/shijarbot", tags=["Shijar Bot"])
@router.get("/")
async def root(request: Request):
    response = await request.json()
    print(response["message"]["text"])