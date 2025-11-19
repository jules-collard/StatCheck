from typing import List

import requests
import polars as pl
from polars import col as c

from .. import BACKEND_URL
from src.models.events import EventBase
from src.analytics.xg.fitting import fit_xg

def set_side_period(group: pl.DataFrame):
    if group.select('homeTeamDefendingSide').to_series().is_null().any():
        ozone_events_home = group.filter(
            c('zoneCode') == 'O',
            c('eventOwnerTeamID') == c('homeTeamID')
        )
        ozone_events_away = group.filter(
            c('zoneCode') == 'O',
            c('eventOwnerTeamID') == c('awayTeamID')
        )
        if ozone_events_home.height > 0:
            if ozone_events_home.row(index = 0, named=True)['xCoord'] < 0:
                defending_side = 'right'
            else:
                defending_side = 'left'
        elif ozone_events_away.height > 0:
            if ozone_events_away.row(index = 0, named=True)['xCoord'] < 0:
                defending_side = 'left'
            else:
                defending_side = 'right'
        else:
            defending_side = None
    else:
        defending_side = None

    return group.with_columns(
        pl.when(c('homeTeamDefendingSide').is_null().any().not_())
        .then(c('homeTeamDefendingSide'))
        .otherwise(pl.lit(defending_side))
        .alias('homeTeamDefendingSide')
    )

def scrape_pbp(gameID: int, neutralSite=False, return_df=False) -> List[EventBase]:
    url = f"https://api-web.nhle.com/v1/gamecenter/{gameID}/play-by-play"

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    
    pbp_df = pl.json_normalize(response["plays"], infer_schema_length=None)
    homeTeamID = response.get('homeTeam', {}).get('id', None)
    awayTeamID = response.get('awayTeam', {}).get('id', None)
    gameType = response.get('gameType', None)
    season = response.get('season', None)
    
    pbp_df = (pbp_df
              .select(pl.all().exclude('details.typeCode'))
              .rename({'periodDescriptor.number':'period'})
              .rename(lambda colname: colname.removeprefix('details.').removeprefix('periodDescriptor.').replace('Id', 'ID'))
              .with_columns(
                  c('timeInPeriod').str.split(":").alias('timeList'),
                  c('situationCode').str.split_exact('', 3).struct.rename_fields(['awayGoalie', 'awaySkaters', 'homeSkaters', 'homeGoalie']).struct.unnest(),
                  c('awayScore').fill_null(strategy='forward').fill_null(strategy='zero').alias('awayScore'),
                  c('homeScore').fill_null(strategy='forward').fill_null(strategy='zero').alias('homeScore'),
                  gameID = gameID,
                  homeTeamID = homeTeamID,
                  awayTeamID = awayTeamID,
                  gameType = gameType,
                  season = season,
                  neutralSite = neutralSite
              )
              .with_columns(
                  (c('timeList').list.first().cast(pl.Int32) * 60 + c('timeList').list.last().cast(pl.Int32)).alias('timeInPeriodSec')
              )
              .group_by('period', maintain_order=True)
              .map_groups(set_side_period)
              .with_columns(
                pl.when(c('homeTeamDefendingSide') == 'right', c('eventOwnerTeamID') == homeTeamID)
                .then(pl.struct(xStd=-c('xCoord'), yStd=-c('yCoord')))
                .when(c('homeTeamDefendingSide') == 'left', c('eventOwnerTeamID') == awayTeamID)
                .then(pl.struct(xStd=-c('xCoord'), yStd=-c('yCoord')))
                .otherwise(pl.struct(xStd=c('xCoord'), yStd=c('yCoord')))
                .struct.unnest()
              ))
    
    if return_df:
        return pbp_df
    
    pbp_df = pbp_df.pipe(fit_xg)
    
    pbp_dicts = pbp_df.to_dicts()
    return [EventBase(**event) for event in pbp_dicts]

def post_event_types():
    event_type_dicts = [
        {'typeCode': 502, 'typeDescKey': 'faceoff'},
        {'typeCode': 503, 'typeDescKey': 'hit'},
        {'typeCode': 504, 'typeDescKey': 'giveaway'},
        {'typeCode': 505, 'typeDescKey': 'goal'},
        {'typeCode': 506, 'typeDescKey': 'shot-on-goal'},
        {'typeCode': 507, 'typeDescKey': 'missed-shot'},
        {'typeCode': 508, 'typeDescKey': 'blocked-shot'},
        {'typeCode': 509, 'typeDescKey': 'penalty'},
        {'typeCode': 516, 'typeDescKey': 'stoppage'},
        {'typeCode': 520, 'typeDescKey': 'period-start'},
        {'typeCode': 521, 'typeDescKey': 'period-end'},
        {'typeCode': 523, 'typeDescKey': 'shootout-complete'},
        {'typeCode': 524, 'typeDescKey': 'game-end'},
        {'typeCode': 525, 'typeDescKey': 'takeaway'},
        {'typeCode': 535, 'typeDescKey': 'delayed-penalty'},
        {'typeCode': 537, 'typeDescKey': 'failed-shot-attempt'}
    ]
    r = requests.post(f"{BACKEND_URL}/games/event-types", json=event_type_dicts)
    print(r.status_code)

def post_pbp(gameID: int, events: List[EventBase]):
    pbp_dicts = [event.model_dump() for event in events]
    r = requests.post(f"{BACKEND_URL}/games/{gameID}/events", json=pbp_dicts)
    print(f"{gameID} Events: {r.status_code}")
