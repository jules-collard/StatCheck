from typing import Annotated
import secrets

import logfire
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.routers import players, admin, teams, games, events, leaderboards, scores, standings
from app.core.config import app_config

app = FastAPI()

if app_config.environment == 'prod':
    logfire.configure(environment=app_config.environment,
                      service_name='backend')
    logfire.instrument_fastapi(app,
                                excluded_urls='/events')
if app_config.environment == 'dev':
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:4200', 'https://localhost:4200'],
        allow_methods=["GET"],
        allow_headers=["*"],
    )

security = HTTPBasic()

def check_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = app_config.username.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = app_config.password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
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
