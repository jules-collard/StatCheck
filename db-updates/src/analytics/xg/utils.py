from typing import Literal

import numpy as np
import polars as pl
from polars import col as c

def last_event_prefix(name: str):
    return f"lastEvent{name[0].capitalize()}{name[1:]}"

def get_shot_angle(x: float, y: float):
    if x is None or y is None:
        return None
    
    ratio = y / np.sqrt(y**2 + (89 - x)**2)
    angle = np.asin(ratio) * 180 / np.pi
    if x > 89 and y >= 0:
        angle = 180 - angle
    elif x > 89 and y < 0:
        angle = -180 - angle
    return 0 if np.isnan(angle) else angle

def get_shot_distance(x: float, y: float):
    return np.sqrt(y**2 + (89-x)**2)

def get_distance_between(x1, y1, x2, y2):
    if any([p is None for p in [x1, y1, x2, y2]]):
        return None
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def get_angle_change_speed(angle1, angle2, time):
    if any([x is None for x in [angle1, angle2, time]]) or time == 0:
        return None
    else:
        return abs(angle2 - angle1) / time
    
def extract_covariates(data: pl.DataFrame, model: Literal['ES', 'PP', 'SH']):
    if model == 'ES':
        return data.select(c('shotDistance'), c('timeSinceLastEvent'), c('shotType'), c('speedFromLastEvent'), c('shotAngle'), c('angleChangeSpeed'), c('lastEventType'), c('defendingSkaters'), c('distFromLastEvent'), c('xStd'), c('yStd'), c('home'), c('homeVenue'), c('gameType'), c('season'))
    elif model == 'PP' or model == 'SH':
        return data.select(c('shotDistance'), c('timeSinceLastEvent'), c('shotType'), c('speedFromLastEvent'), c('shotAngle'), c('angleChangeSpeed'), c('lastEventType'), c('manAdvantage'), c('defendingSkaters'), c('distFromLastEvent'), c('xStd'), c('yStd'), c('home'), c('homeVenue'), c('gameType'), c('season'))

def extract_target(data: pl.DataFrame):
    return data.select(c('isGoal')).to_series()

def extract_indices(data: pl.DataFrame):
    return data.select(c('gameID'), c('eventID'))
