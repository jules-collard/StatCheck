from fastapi import APIRouter, status
from pydantic import BaseModel

class TestModel(BaseModel):
    id: int
    body: str


router = APIRouter(prefix='/api/healthcheck')

@router.get('/', status_code=200)
def return_check():
    return {"status": "healthy"}

@router.put('/', status_code=status.HTTP_200_OK)
def put_check(obj: TestModel):
    return {"obj": obj}