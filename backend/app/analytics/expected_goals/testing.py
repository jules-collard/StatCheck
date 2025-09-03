import os
import xgboost as xgb
from sklearn.metrics import log_loss

from .cleaning import clean_data, load_seasons, transform_data

def load_model(name: str):
    mod = xgb.XGBClassifier()
    mod.load_model(os.path.join(os.path.dirname(__file__), "models", f"{name}.json"))
    return mod

def predict(X_test, y_test, mod, name):
    y_pred = mod.predict_proba(X_test)
    predictions = X_test.copy()
    predictions['isGoal'] = y_test
    predictions['xg'] = y_pred[:,1]

    predictions.to_pickle(os.path.join(os.path.dirname(__file__), "models", f"{name}.pkl"))

    print(log_loss(y_test, y_pred))

if __name__ == "__main__":
    data = load_seasons(20172018, 20172018)
    es_data, pp_data, sh_data = clean_data(data)

    ev_mod = load_model("ES_model")
    X_test_es, y_test_es, _ = transform_data(es_data, model='ES')
    predict(X_test_es, y_test_es, ev_mod, "ES_predictions")

    pp_mod = load_model("PP_model")
    X_test_pp, y_test_pp, _ = transform_data(pp_data, model='PP')
    predict(X_test_pp, y_test_pp, pp_mod, "PP_predictions")

    sh_mod = load_model("SH_model")
    X_test_sh, y_test_sh, _ = transform_data(sh_data, model='SH')
    predict(X_test_sh, y_test_sh, sh_mod, "SH_predictions")