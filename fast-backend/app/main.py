import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import players, admin, teams, games, events, leaderboards, scores, standings

app = FastAPI()

logfire.configure()
logfire.instrument_fastapi(app)

origins = [
    'http://localhost:8080',
    'https://localhost:8080',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(players.router, prefix='/api')
app.include_router(teams.router, prefix='/api')
app.include_router(games.router, prefix='/api')
app.include_router(admin.router, prefix='/api')
app.include_router(events.router, prefix='/api')
app.include_router(leaderboards.router, prefix='/api')
app.include_router(scores.router, prefix='/api')
app.include_router(standings.router, prefix='/api')

@app.get("/")
async def root():
    return {"message": "Hello World"}
