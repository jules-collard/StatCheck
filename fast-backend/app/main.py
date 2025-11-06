from fastapi import FastAPI

from .routers import players

app = FastAPI()

app.include_router(players.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
