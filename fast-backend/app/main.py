from fastapi import FastAPI

from .routers import players, test

app = FastAPI()

app.include_router(players.router)
app.include_router(test.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
