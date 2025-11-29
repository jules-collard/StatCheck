import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import players, admin, teams, games, events, leaderboards, scores, standings
from app.core.config import app_config

app = FastAPI()

if app_config.environment == 'prod':
    logfire.configure(environment=app_config.environment,
                      service_name='backend')
    logfire.instrument_fastapi(app,
                               excluded_urls='^/events')
if app_config.environment == 'dev':
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=["GET"],
        allow_headers=["*"],
    )

app.include_router(players.router)
app.include_router(teams.router)
app.include_router(games.router)
app.include_router(admin.router)
app.include_router(events.router)
app.include_router(leaderboards.router)
app.include_router(scores.router)
app.include_router(standings.router)

app.include_router(players.router, prefix="/api")
app.include_router(teams.router, prefix="/api")
app.include_router(games.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(leaderboards.router, prefix="/api")
app.include_router(scores.router, prefix="/api")
app.include_router(standings.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World"}
