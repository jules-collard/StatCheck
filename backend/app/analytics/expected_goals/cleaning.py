from sklearn.impute import SimpleImputer
from app import app, db
from app.models import Event, Game

import pandas as pd
import numpy as np
import polars as pl
from polars import col as c
from typing import Literal
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

TYPECODES = {
    502: 'faceoff',
    502: 'hit',
    504: 'giveaway',
    505: 'goal',
    506: 'shot-on-goal',
    507: 'missed-shot',
    508: 'blocked-shot',
    525: 'takeaway',
    537: 'failed-shot-attempt'
}

SHOTTYPES = ['backhand', 'deflected', 'slap', 'snap', 'tip-in', 'wrap-around', 'wrist']

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

def set_side(data: pl.DataFrame, preserve_order = False):
    return data.group_by('gameID', 'period', maintain_order=preserve_order).map_groups(set_side_period)

def standardise_coordinates(data: pl.DataFrame):
    return data.with_columns(
        pl.when(c('homeTeamDefendingSide') == 'right', c('eventOwnerTeamID') == c('homeTeamID'))
        .then(pl.struct(xStd=-c('xCoord'), yStd=-c('yCoord'), lastEventXStd=-c('lastEventXCoord'), lastEventYStd=-c('lastEventYCoord')))
        .when(c('homeTeamDefendingSide') == 'left', c('eventOwnerTeamID') == c('awayTeamID'))
        .then(pl.struct(xStd=-c('xCoord'), yStd=-c('yCoord'), lastEventXStd=-c('lastEventXCoord'), lastEventYStd=-c('lastEventYCoord')))
        .otherwise(pl.struct(xStd=c('xCoord'), yStd=c('yCoord'), lastEventXStd=c('lastEventXCoord'), lastEventYStd=c('lastEventYCoord')))
        .struct.unnest()
    )

def add_last_event(data: pl.DataFrame):
    return data.with_columns(
        c("timeInPeriodSec", "typeCode", "xCoord", "yCoord", "eventOwnerTeamID").shift(1).over("gameID", "period").name.map(last_event_prefix)
    ).with_columns(
        timeSinceLastEvent = c("timeInPeriodSec") - c("lastEventTimeInPeriodSec"),
        distFromLastEvent = pl.struct(["xCoord", "yCoord", "lastEventXCoord", "lastEventYCoord"])
                              .map_elements(lambda s: get_distance_between(s["xCoord"], s["yCoord"], s["lastEventXCoord"], s["lastEventYCoord"]), return_dtype=pl.Float64)
    ).with_columns(
        speedFromLastEvent = c("distFromLastEvent") / c("timeSinceLastEvent")
    ).select(
        pl.all().exclude("lastEventTimeInPeriodSec")
    )

def last_event_prefix(name: str):
    return f"lastEvent{name[0].capitalize()}{name[1:]}"

def add_shot_information(data: pl.DataFrame):
    return data.with_columns(
        isGoal = (c('typeCode') == 505).cast(pl.Int8),
        shotAngle = pl.struct(['xStd', 'yStd']).map_elements(lambda s: get_shot_angle(s['xStd'], s['yStd']), return_dtype=pl.Float64),
        shotDistance = pl.struct(['xStd', 'yStd']).map_elements(lambda s: get_shot_distance(s['xStd'], s['yStd']), return_dtype=pl.Float64),
        lastShotAngle = (pl.when(c('lastEventTypeCode') == 506, c('timeSinceLastEvent') < 3, c('eventOwnerTeamID') == c('lastEventEventOwnerTeamID'))
                         .then(pl.struct(['lastEventXStd', 'lastEventYStd']).map_elements(lambda s: get_shot_angle(s['lastEventXStd'], s['lastEventYStd']),
                                                                                          return_dtype=pl.Float64))
        )
    ).with_columns(
        angleChangeSpeed = pl.struct(['lastShotAngle', 'shotAngle', 'timeSinceLastEvent']).map_elements(lambda s: get_angle_change_speed(s['lastShotAngle'], s['shotAngle'], s['timeSinceLastEvent']), return_dtype=pl.Float64)
    )

def add_strengths(data: pl.DataFrame):
    return data.with_columns(
        attackingSkaters = (pl.when(c('eventOwnerTeamID') == c('homeTeamID'))
                            .then(c('homeSkaters'))
                            .otherwise(c('awaySkaters'))),
        defendingSkaters = (pl.when(c('eventOwnerTeamID') == c('homeTeamID'))
                            .then(c('awaySkaters'))
                            .otherwise(c('homeSkaters'))),
        goalieInNet = (pl.when(c('eventOwnerTeamID') == c('homeTeamID'))
                        .then(c('awayGoalie'))
                        .otherwise(c('homeGoalie')))
    ).with_columns(
        manAdvantage = c('attackingSkaters') - c('defendingSkaters')
    )

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

def get_speed(x1, y1, x2, y2, time):
    if any([np.isnan(num) for num in [x1, y1, x2, y2, time]]) or time == 0:
        return np.nan
    
    dist = get_distance_between(x1, y1, x2, y2)
    return dist / time

def get_angle_change_speed(angle1, angle2, time):
    if any([x is None for x in [angle1, angle2, time]]) or time == 0:
        return None
    else:
        return abs(angle2 - angle1) / time

def typecode_descriptions(data: pl.DataFrame):
    return data.with_columns(
        c('lastEventTypeCode').replace_strict(TYPECODES, return_dtype=pl.String).alias('lastEventTypeCode')
    )

def extract_covariates(data: pl.DataFrame, model: Literal['ES', 'PP']):
    if model == 'ES':
        return data.select(c('shotDistance'), c('timeSinceLastEvent'), c('shotType'), c('speedFromLastEvent'), c('shotAngle'), c('angleChangeSpeed'), c('lastEventTypeCode'), c('defendingSkaters'), c('distFromLastEvent'), c('xStd'), c('yStd'))
    elif model == 'PP':
        return data.select(c('shotDistance'), c('timeSinceLastEvent'), c('shotType'), c('speedFromLastEvent'), c('shotAngle'), c('angleChangeSpeed'), c('lastEventTypeCode'), c('manAdvantage'), c('defendingSkaters'), c('distFromLastEvent'), c('xStd'), c('yStd'))

def extract_target(data: pl.DataFrame):
    return data.select(c('isGoal')).to_series()

def extract_indices(data: pl.DataFrame):
    return data.select(c('gameID'), c('id'))

def clean_data(season: int, remove_empty_net = True, strength_state: Literal["ES", "PP", "SH", "ALL"] = "ALL") -> pl.DataFrame:
    app.app_context().push()
    data = (db.session.query(Event.gameID, Event.id, Event.timeInPeriodSec, Event.sortOrder, Event.typeCode, Event.awayGoalie, Event.awaySkaters, Event.homeGoalie, Event.homeSkaters, Event.homeTeamDefendingSide, Event.period, Event.eventOwnerTeamID, Event.shootingPlayerID, Event.xCoord, Event.yCoord, Event.zoneCode, Event.shotType, Game.homeTeamID, Game.awayTeamID)
            .filter(Game.season == season)
            .filter(Game.gameType == 2)
            .filter(Event.periodType != 'SO')
            .filter(Event.typeCode.in_(TYPECODES.keys()))
            .join(Event.game)
            .order_by(Game.id, Event.period, Event.timeInPeriodSec, Event.sortOrder)
            .all())
    
    data = pl.DataFrame(data)
    data = (data
            .pipe(add_last_event)
            .filter(c('typeCode').is_in([505,506,507]))
            .pipe(set_side)
            .drop_nulls(subset = ['xCoord', 'yCoord'])
            .pipe(standardise_coordinates)
            .filter(c('xStd') > -25)
            .pipe(add_shot_information)
            .pipe(add_strengths)
            .filter(c('defendingSkaters') > 0)
            .pipe(typecode_descriptions)
    )

    if remove_empty_net: data = data.filter(c('goalieInNet') > 0)
    if strength_state == "ES":
        data = data.filter(c('manAdvantage') == 0)
    elif strength_state == "PP":
        data = data.filter(c('manAdvantage') > 0)
    elif strength_state == "SH":
        data = data.filter(c('manAdvantage') < 0)

    return data
    
def transform_data(data: pl.DataFrame, model: Literal['ES', 'PP']):
    features = data.pipe(extract_covariates, model).to_pandas()
    target = data.pipe(extract_target)
    index = data.pipe(extract_indices)

    typecode_categories = [*TYPECODES.values(), 'missing']
    shottype_categories = [*SHOTTYPES, 'missing']

    categorical_transformer = Pipeline(steps=[
        ('nan-imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('none-imputer', SimpleImputer(strategy='constant', missing_values=None, fill_value='missing')),
        ('onehot', OneHotEncoder(categories=[typecode_categories, shottype_categories]))
    ])

    categorical_features = ['lastEventTypeCode', 'shotType']
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough',
        verbose_feature_names_out=False
    )

    transformed_features = preprocessor.fit_transform(features)
    feature_names = preprocessor.get_feature_names_out()
    transformed_df = pd.DataFrame(transformed_features, columns=feature_names).astype(float)

    return transformed_df, target, index

if __name__ == "__main__":
    data = clean_data(20142015)
    x, y, z = transform_data(data, model = 'ES')
    print(x.head(20))