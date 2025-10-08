from typing import Literal

import sqlalchemy as sa
import numpy as np
import polars as pl
from polars import col as c
from scipy.sparse import csr_matrix
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from app import app, db
from app.models import Event, Game

TYPECODES = {
    502: 'faceoff',
    503: 'hit',
    504: 'giveaway',
    505: 'goal',
    506: 'shot-on-goal',
    507: 'missed-shot',
    508: 'blocked-shot',
    525: 'takeaway',
    537: 'failed-shot-attempt'
}

SHOTTYPES = ['wrist', 'tip-in', 'snap', 'slap', 'poke', 'backhand', 'bat', 'deflected', 'wrap-around', 'between-legs', 'cradle']

GAMETYPES = ['REG', 'POST']

TEAMS = ['10', '5', '30', '21', '22', '29', '1', '12', '17', '9', '11', '6', '7', '2', '15', '14', '19', '18', '16', '28', '23', '27', '20', '4', '26', '8', '24', '25', '3', '13', '52', '53', '54', '55', '59']

SEASONS = ['20102011', '20112012', '20122013', '20132014', '20142015', '20152016', '20162017', '20172018', '20182019', '20192020', '20202021', '20212022', '20222023', '20232024', '20242025', '20252026']
MODEL_SEASONS = ['20102011', '20112012', '20122013', '20132014', '20142015', '20152016', '20162017', '20172018', '20182019', '20192020', '20202021', '20212022', '20222023', '20232024', '20242025']

teams_enum = pl.Enum(TEAMS)
seasons_enum = pl.Enum(SEASONS)

schema = {
    'gameID': pl.Categorical,
    'id': pl.Int64,
    'timeInPeriodSec': pl.Int16,
    'typeCode': pl.Int16,
    'awayGoalie': pl.Int8,
    'awaySkaters': pl.Int8,
    'homeGoalie': pl.Int8,
    'homeSkaters': pl.Int8,
    'homeTeamDefendingSide': pl.Enum(['left', 'right']),
    'period': pl.Int8,
    'eventOwnerTeamID': teams_enum,
    'shootingPlayerID': pl.Int64,
    'xCoord': pl.Float64,
    'yCoord': pl.Float64,
    'zoneCode': pl.Enum(['D', 'N', 'O']),
    'shotType': pl.Enum(SHOTTYPES),
    'homeTeamID': teams_enum,
    'awayTeamID': teams_enum,
    'gameType': pl.Int8,
    'neutralSite': pl.Boolean,
    'season': seasons_enum
}

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
    ).select(pl.all().exclude(['xCoord', 'yCoord', 'lastEventXCoord', 'lastEventYCoord']))

def add_last_event(data: pl.DataFrame):
    return data.with_columns(
        c("timeInPeriodSec", "typeCode", "xCoord", "yCoord", "eventOwnerTeamID").shift(1).over("gameID", "period").name.map(last_event_prefix)
    ).with_columns(
        timeSinceLastEvent = (c("timeInPeriodSec") - c("lastEventTimeInPeriodSec")),
        distFromLastEvent = pl.struct(["xCoord", "yCoord", "lastEventXCoord", "lastEventYCoord"])
                              .map_elements(lambda s: get_distance_between(s["xCoord"], s["yCoord"], s["lastEventXCoord"], s["lastEventYCoord"]), return_dtype=pl.Float64)
    ).with_columns(
        speedFromLastEvent = pl.when(c('timeSinceLastEvent') != 0).then(c("distFromLastEvent") / c("timeSinceLastEvent"))
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
    ).select(pl.all().exclude('lastShotAngle'))

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

def add_home_away(data: pl.DataFrame):
    return data.with_columns(
        home = (c('eventOwnerTeamID') == c('homeTeamID'))
    )

def add_venue(data: pl.DataFrame):
    return data.with_columns(
        pl.when(c('neutralSite') == 0)
        .then(c('homeTeamID').cast(pl.String))
        .otherwise(pl.lit('neutral'))
        .alias('homeVenue')
    ).select(pl.all().exclude('neutralSite'))

def clean_seasons(data: pl.DataFrame, last_season: str):
    return data.with_columns(
        pl.when(c('season') > pl.lit(last_season))
        .then(pl.lit(last_season))
        .otherwise(c('season'))
        .cast(seasons_enum)
        .alias('season')
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

def get_angle_change_speed(angle1, angle2, time):
    if any([x is None for x in [angle1, angle2, time]]) or time == 0:
        return None
    else:
        return abs(angle2 - angle1) / time

def typecode_descriptions(data: pl.DataFrame):
    return data.with_columns(
        c('lastEventTypeCode').replace_strict(TYPECODES, return_dtype=pl.String).alias('lastEventType')
    ).select(pl.all().exclude('lastEventTypeCode'))

def gametype_descriptions(data: pl.DataFrame):
    return data.with_columns(
        c('gameType').replace_strict({2: 'REG', 3: 'POST'}).alias('gameType')
    )

def extract_covariates(data: pl.DataFrame, model: Literal['ES', 'PP', 'SH']):
    if model == 'ES':
        return data.select(c('shotDistance'), c('timeSinceLastEvent'), c('shotType'), c('speedFromLastEvent'), c('shotAngle'), c('angleChangeSpeed'), c('lastEventType'), c('defendingSkaters'), c('distFromLastEvent'), c('xStd'), c('yStd'), c('home'), c('homeVenue'), c('gameType'), c('season'))
    elif model == 'PP' or model == 'SH':
        return data.select(c('shotDistance'), c('timeSinceLastEvent'), c('shotType'), c('speedFromLastEvent'), c('shotAngle'), c('angleChangeSpeed'), c('lastEventType'), c('manAdvantage'), c('defendingSkaters'), c('distFromLastEvent'), c('xStd'), c('yStd'), c('home'), c('homeVenue'), c('gameType'), c('season'))

def extract_target(data: pl.DataFrame):
    return data.select(c('isGoal')).to_series()

def extract_indices(data: pl.DataFrame):
    return data.select(c('gameID'), c('id'))

def load_seasons(start_season: int, end_season: int) -> pl.DataFrame:
    app.app_context().push()
    data = (db.session.query(Event.gameID, Event.id, Event.timeInPeriodSec, Event.typeCode, Event.awayGoalie, Event.awaySkaters, Event.homeGoalie, Event.homeSkaters, Event.homeTeamDefendingSide, Event.period, Event.eventOwnerTeamID, Event.shootingPlayerID, Event.xCoord, Event.yCoord, Event.zoneCode, Event.shotType, Game.homeTeamID, Game.awayTeamID, Game.gameType, Game.neutralSite, Game.season)
            .filter(sa.and_(Game.season >= start_season, Game.season <= end_season))
            .filter(sa.or_(Game.gameType == 2, Game.gameType == 3))
            .filter(Event.periodType != 'SO')
            .filter(Event.typeCode.in_(TYPECODES.keys()))
            .join(Event.game)
            .order_by(Game.id, Event.period, Event.timeInPeriodSec, Event.sortOrder)
            .all())
    
    data = pl.DataFrame(data, schema=schema)
    return data

def load_games(id_list: list[int]) -> pl.DataFrame:
    app.app_context().push()
    data = (db.session.query(Event.gameID, Event.id, Event.timeInPeriodSec, Event.typeCode, Event.awayGoalie, Event.awaySkaters, Event.homeGoalie, Event.homeSkaters, Event.homeTeamDefendingSide, Event.period, Event.eventOwnerTeamID, Event.shootingPlayerID, Event.xCoord, Event.yCoord, Event.zoneCode, Event.shotType, Game.homeTeamID, Game.awayTeamID, Game.gameType, Game.neutralSite, Game.season)
            .filter(Game.id.in_(id_list))
            .filter(sa.or_(Game.gameType == 2, Game.gameType == 3))
            .filter(Event.periodType != 'SO')
            .filter(Event.typeCode.in_(TYPECODES.keys()))
            .join(Event.game)
            .order_by(Game.id, Event.period, Event.timeInPeriodSec, Event.sortOrder)
            .all())
    
    data = pl.DataFrame(data, schema=schema)
    return data

def clean_data(data: pl.DataFrame, remove_empty_net = True):
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
            .pipe(gametype_descriptions)
            .pipe(add_home_away)
            .pipe(add_venue)
            .pipe(clean_seasons, last_season = '20242025')
    )

    if remove_empty_net:
        data = data.filter(c('goalieInNet') > 0)

    es_data = data.filter(c('manAdvantage') == 0)
    pp_data = data.filter(c('manAdvantage') > 0)
    sh_data = data.filter(c('manAdvantage') < 0)

    return es_data, pp_data, sh_data
    
def transform_data(data: pl.DataFrame, model: Literal['ES', 'PP', 'SH']):
    features = data.pipe(extract_covariates, model).to_pandas()
    target = data.pipe(extract_target)
    index = data.pipe(extract_indices)

    typecode_categories = [*TYPECODES.values(), 'missing']
    shottype_categories = [*SHOTTYPES, 'missing']
    homevenue_categories = [*TEAMS, 'neutral']

    categorical_transformer = Pipeline(steps=[
        ('nan-imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('none-imputer', SimpleImputer(strategy='constant', missing_values=None, fill_value='missing')),
        ('onehot', OneHotEncoder(categories=[typecode_categories, shottype_categories, MODEL_SEASONS, GAMETYPES, homevenue_categories]))
    ])

    categorical_features = ['lastEventType', 'shotType', 'season', 'gameType', 'homeVenue']
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough',
        verbose_feature_names_out=False
    )

    transformed_features: csr_matrix = preprocessor.fit_transform(features)
    feature_names = preprocessor.get_feature_names_out().tolist()
    transformed_df = pl.DataFrame(transformed_features.toarray(), schema=feature_names).cast(pl.Float64)

    return transformed_df, target, index

if __name__ == "__main__":
    data = load_games([2025020001, 2025020002, 2025020001])
    data = clean_data(data)
    print(data[0].select(c('season')))

