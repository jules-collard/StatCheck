import os
from typing import Literal

import polars as pl
from polars import col as c
from scipy.sparse import csr_matrix
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import xgboost as xgb

from .utils import last_event_prefix, get_angle_change_speed, get_distance_between, get_shot_angle, get_shot_distance, extract_covariates, extract_target, extract_indices

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
TEAMS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 52, 53, 54, 55, 59]
SEASONS = [20102011, 20112012, 20122013, 20132014, 20142015, 20152016, 20162017, 20172018, 20182019, 20192020, 20202021, 20212022, 20222023, 20232024, 20242025]

schema = {
    'gameID': pl.Int64,
    'eventID': pl.Int64,
    'timeInPeriodSec': pl.Int16,
    'typeCode': pl.Int16,
    'awayGoalie': pl.Int8,
    'awaySkaters': pl.Int8,
    'homeGoalie': pl.Int8,
    'homeSkaters': pl.Int8,
    'homeTeamDefendingSide': pl.Enum(['left', 'right']),
    'period': pl.Int8,
    'periodType': pl.Enum(['REG', 'OT', 'SO']),
    'eventOwnerTeamID': pl.Int16,
    'shootingPlayerID': pl.Int64,
    'xCoord': pl.Float64,
    'yCoord': pl.Float64,
    'zoneCode': pl.Enum(['D', 'N', 'O']),
    'shotType': pl.Enum(SHOTTYPES),
    'homeTeamID': pl.Int16,
    'awayTeamID': pl.Int16,
    'gameType': pl.Int8,
    'neutralSite': pl.Boolean,
    'season': pl.Int64
}

def load_model(name: str):
    mod = xgb.XGBClassifier()
    mod.load_model(os.path.join(os.path.dirname(__file__), "models", f"{name}.json"))
    return mod

def add_last_event(data: pl.DataFrame):
    return data.with_columns(
        c("timeInPeriodSec", "typeCode", "xCoord", "yCoord", "xStd", "yStd", "eventOwnerTeamID").shift(1).over("gameID", "period").name.map(last_event_prefix)
    ).with_columns(
        timeSinceLastEvent = (c("timeInPeriodSec") - c("lastEventTimeInPeriodSec")),
        distFromLastEvent = pl.struct(["xCoord", "yCoord", "lastEventXCoord", "lastEventYCoord"])
                              .map_elements(lambda s: get_distance_between(s["xCoord"], s["yCoord"], s["lastEventXCoord"], s["lastEventYCoord"]), return_dtype=pl.Float64)
    ).with_columns(
        speedFromLastEvent = pl.when(c('timeSinceLastEvent') != 0).then(c("distFromLastEvent") / c("timeSinceLastEvent"))
    ).select(
        pl.all().exclude("lastEventTimeInPeriodSec")
    )

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

def clean_data(data: pl.DataFrame):
    shots = (data
             .cast(schema, strict=False)
             .filter(
                 c('periodType').is_in(['REG', 'OT']),
                 c('typeCode').is_in(TYPECODES.keys())
             )
             .sort(c('gameID'), c('period'), c('timeInPeriodSec'), c('sortOrder'))
             .pipe(add_last_event)
             .filter(c('typeCode').is_in([505,506,507]),
                     c('xStd') > -25)
             .drop_nulls(subset=['xStd', 'yStd'])
             .pipe(add_shot_information)
             .pipe(add_strengths)
             .filter(c('defendingSkaters') > 0, c('goalieInNet') > 0)
             .with_columns(
                 c('lastEventTypeCode').replace_strict(TYPECODES, return_dtype=pl.String).alias('lastEventType'),
                 c('gameType').replace_strict({2: 'REG', 3: 'POST'}).alias('gameType'),
                 pl.when(c('neutralSite') | c('homeTeamID').is_in(TEAMS).not_()).then(None).otherwise(c('homeTeamID').cast(pl.String)).alias('homeVenue'),
                 pl.when(c('season').is_in(SEASONS).not_()).then(max(SEASONS)).otherwise(c('season')).alias('season'),
                 home = (c('eventOwnerTeamID') == c('homeTeamID'))
             ))
    
    es_data = shots.filter(c('manAdvantage') == 0)
    pp_data = shots.filter(c('manAdvantage') > 0)
    sh_data = shots.filter(c('manAdvantage') < 0)

    return es_data, pp_data, sh_data

def transform_data(data: pl.DataFrame, model: Literal['ES', 'PP', 'SH']):
    features = data.pipe(extract_covariates, model).to_pandas()
    target = data.pipe(extract_target)
    index = data.pipe(extract_indices)

    typecode_categories = [*TYPECODES.values(), 'missing']
    shottype_categories = [*SHOTTYPES, 'missing']
    homevenue_categories = [*[str(team) for team in TEAMS], 'neutral']

    categorical_transformer = Pipeline(steps=[
        ('nan-imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('none-imputer', SimpleImputer(strategy='constant', missing_values=None, fill_value='missing')),
        ('onehot', OneHotEncoder(categories=[typecode_categories, shottype_categories, GAMETYPES, SEASONS]))
    ])

    homevenue_transformer = Pipeline(steps=[
        ('null-imputer', SimpleImputer(strategy='constant', missing_values=None, fill_value='neutral')),
        ('onehot', OneHotEncoder(categories=[homevenue_categories]))
    ])

    categorical_features = ['lastEventType', 'shotType', 'gameType', 'season']
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features),
            ('venue', homevenue_transformer, ['homeVenue']),
        ],
        remainder='passthrough',
        verbose_feature_names_out=False
    )

    transformed_features: csr_matrix = preprocessor.fit_transform(features)
    feature_names = preprocessor.get_feature_names_out().tolist()
    transformed_df = pl.DataFrame(transformed_features.toarray(), schema=feature_names).cast(pl.Float64)

    return transformed_df, target, index

def calculate_xg(data: pl.DataFrame, model: xgb.XGBClassifier, model_name: Literal['ES', 'PP', 'SH']) -> pl.DataFrame:
    if data.is_empty():
        return pl.DataFrame({'gameID': [], 'eventID': [], 'xg': []})
    
    X_test, _, index = transform_data(data, model=model_name)
    xg_fit = model.predict_proba(X_test)
    return index.with_columns(xg = xg_fit[:,1])

def fit_xg(data: pl.DataFrame, join=True):
    es_shots, pp_shots, sh_shots = clean_data(data)

    es_mod = load_model('ES_model')
    pp_mod = load_model('PP_model')
    sh_mod = load_model('SH_model')

    es_xg = calculate_xg(es_shots, es_mod, 'ES')
    pp_xg = calculate_xg(pp_shots, pp_mod, 'PP')
    sh_xg = calculate_xg(sh_shots, sh_mod, 'SH')

    xg = pl.concat([es_xg, pp_xg, sh_xg])
    
    if join:
        return data.join(xg, on=['gameID','eventID'], how='left')
    else:
        return xg
