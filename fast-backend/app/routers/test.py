from fastapi import APIRouter

router = APIRouter()

@router.get('/test', status_code=200)
def return_test():
    return {"message": "success"}