from fastapi import APIRouter, Request

router = APIRouter(prefix="/shijarbot", tags=["Shijar Bot"])


@router.post("/")
async def root(request: Request):
    response = await request.json()
    print(response["message"]["text"])


@router.get("/")
async def demo_bot():
    return {"message": "Telegram Webhook"}
