from typing import List

import requests
import polars as pl
from polars import col as c

from .. import BACKEND_URL
from src.models.shifts import ShiftBase

def scrape_shifts(gameID: int):
    url = f"https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={gameID}"

    response = requests.get(url)
    response.raise_for_status()
    response = response.json()

    shifts: pl.DataFrame = pl.json_normalize(response.get('data', {}), infer_schema_length=None)
    if shifts.is_empty():
        return {}
    
    shifts = (shifts
              .rename({'playerId':'playerID', 'gameId':'gameID', 'teamId':'teamID'})
              .filter(c('detailCode') == 0, c('typeCode') == 517)
              .with_columns(
                  c('duration').str.split(':').alias('durationList'),
                  c('startTime').str.split(':').alias('startTimeList'),
                  c('endTime').str.split(':').alias('endTimeList'),
              )
              .with_columns(
                  durationSec = (c('durationList').list.first().cast(pl.Int32) * 60 + c('durationList').list.last().cast(pl.Int32)),
                  startTimeSec = (c('startTimeList').list.first().cast(pl.Int32) * 60 + c('startTimeList').list.last().cast(pl.Int32)),
                  endTimeSec = (c('endTimeList').list.first().cast(pl.Int32) * 60 + c('endTimeList').list.last().cast(pl.Int32)),
              ))
    
    shift_dicts = shifts.to_dicts()
    return [ShiftBase(**shift) for shift in shift_dicts]

def post_shifts(gameID: int, shifts: List[ShiftBase]):
    data = [shift.model_dump() for shift in shifts]
    r = requests.post(f"{BACKEND_URL}/games/{gameID}/shifts", json=data)
    print(f"{gameID} Shifts: {r.status_code}")

if __name__ == "__main__":
    shifts = scrape_shifts(2025020260)
    print([shift for shift in shifts if shift.id == 15733052])
