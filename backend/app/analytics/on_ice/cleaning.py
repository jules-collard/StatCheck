import polars as pl
import polars.selectors as cs
from polars import col as c

def add_faceoff_zone(data: pl.DataFrame):
    q = data.lazy().with_columns(
        faceoffZone = pl.when(c('homeTeamID') == c('teamID'), ((c('homeTeamDefendingSide') == 'right') & (c('xCoord') > 25)) | ((c('homeTeamDefendingSide') == 'left') & (c('xCoord') < -25)))
                    .then(pl.lit('D'))
                    .when(c('homeTeamID') == c('teamID'), ((c('homeTeamDefendingSide') == 'right') & (c('xCoord') < -25)) | ((c('homeTeamDefendingSide') == 'left') & (c('xCoord') > 25)))
                    .then(pl.lit('O'))
                    .when(c('homeTeamID') != c('teamID'), ((c('homeTeamDefendingSide') == 'right') & (c('xCoord') < -25)) | ((c('homeTeamDefendingSide') == 'left') & (c('xCoord') > 25)))
                    .then(pl.lit('D'))
                    .when(c('homeTeamID') != c('teamID'), ((c('homeTeamDefendingSide') == 'right') & (c('xCoord') > 25)) | ((c('homeTeamDefendingSide') == 'left') & (c('xCoord') < -25)))
                    .then(pl.lit('O'))
                    .when(c('homeTeamDefendingSide').is_null() | c('xCoord').is_null() | (c('typeCode') != 502))
                    .then(None)
                    .otherwise(pl.lit('N'))
                    .cast(pl.Enum(['D', 'N', 'O']))
    )
    return q.collect()

def add_strengths(data: pl.DataFrame):
    return (data.lazy()
            .with_columns(attackingSkaters = pl.when(c('homeTeamID') == c('teamID')).then(c('homeSkaters')).otherwise(c('awaySkaters')),
                          defendingSkaters = pl.when(c('homeTeamID') == c('teamID')).then(c('awaySkaters')).otherwise(c('homeSkaters')),
                          attackingGoalie = pl.when(c('homeTeamID') == c('teamID')).then(c('homeGoalie')).otherwise(c('awayGoalie')),
                          defendingGoalie = pl.when(c('homeTeamID') == c('teamID')).then(c('awayGoalie')).otherwise(c('homeGoalie')))
            .with_columns(manAdvantage = c('attackingSkaters') - c('defendingSkaters'),
                          strengthState = pl.struct(['attackingSkaters', 'defendingSkaters', 'attackingGoalie', 'defendingGoalie']))
            .with_columns(split = c('manAdvantage').rle_id().over('shiftID'))
            .drop('xCoord', 'homeTeamDefendingSide', cs.contains('Goalie', 'Skaters'))
            .collect())