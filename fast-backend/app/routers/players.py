from fastapi import APIRouter

router = APIRouter()

@router.get('/players/{name}')
async def read_player(name: str):
    return {"name": name}