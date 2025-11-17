from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .routers import players, check, teams, games

app = FastAPI()

app.include_router(players.router, prefix='/api')
app.include_router(teams.router, prefix='/api')
app.include_router(games.router, prefix='/api')
app.include_router(check.router, prefix='/api')

@app.get("/")
async def root():
    return {"message": "Hello World"}
