from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .routers import players, check, teams

app = FastAPI()

app.include_router(players.router)
app.include_router(teams.router)
app.include_router(check.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}
