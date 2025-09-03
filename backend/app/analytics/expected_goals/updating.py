import polars as pl
from typing import Literal
import xgboost as xgb
import sqlalchemy as sa

from app import app, db
from app.models import Event

from .cleaning import load_games, load_seasons, clean_data, transform_data
from .testing import load_model

def calculate_xg(data: pl.DataFrame, model: xgb.XGBClassifier, model_name: Literal['ES', 'PP', 'SH']) -> pl.DataFrame:
    if data.height == 0: return pl.DataFrame({'gameID': [], 'id': [], 'xg': []})
    
    X_test, _, index = transform_data(data, model=model_name)
    xg_fit = model.predict_proba(X_test)
    return index.with_columns(xg = xg_fit[:,1])

def insert_xg(data: pl.DataFrame):
    es_shots, pp_shots, sh_shots = clean_data(data)

    es_mod = load_model('ES_model')
    pp_mod = load_model('PP_model')
    sh_mod = load_model('SH_model')

    es_xg = calculate_xg(es_shots, es_mod, 'ES')
    pp_xg = calculate_xg(pp_shots, pp_mod, 'PP')
    sh_xg = calculate_xg(sh_shots, sh_mod, 'SH')

    xg = pl.concat([es_xg, pp_xg, sh_xg])

    mappings = xg.to_dicts()
    db.session.execute(sa.update(Event), mappings)
    db.session.commit()

if __name__ == "__main__":
    app.app_context().push()
    data = load_seasons(20242025, 20242025)
    insert_xg(data)
    