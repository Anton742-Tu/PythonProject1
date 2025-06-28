from fastapi import APIRouter


router = APIRouter()


@router.get("/events")
async def get_events():
    return {"events": ["Акция на кешбэк", "Новые категории инвестиций"]}
