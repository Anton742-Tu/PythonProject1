from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def home():
    return {"message": "Добро пожаловать в анализатор транзакций!"}
