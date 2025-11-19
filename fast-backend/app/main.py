from fastapi import FastAPI

from .routers import players, check, teams, games, events

app = FastAPI()

app.include_router(players.router, prefix='/api')
app.include_router(teams.router, prefix='/api')
app.include_router(games.router, prefix='/api')
app.include_router(check.router, prefix='/api')
app.include_router(events.router, prefix='/api')

@app.get("/")
async def root():
    return {"message": "Hello World"}
