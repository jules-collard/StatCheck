import os
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.metrics import log_loss, roc_auc_score, roc_curve

from .cleaning import clean_data, transform_data

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
    ev_mod = load_model("ES_model")
    even_strength = clean_data(20172018, 20172018, strength_state='ES')
    X_test_es, y_test_es = transform_data(even_strength, model='ES')
    predict(X_test_es, y_test_es, ev_mod, "ES_predictions")

    pp_mod = load_model("PP_model")
    powerplay = clean_data(20172018, 20172018, strength_state='PP')
    X_test_pp, y_test_pp = transform_data(powerplay, model='PP')
    predict(X_test_pp, y_test_pp, pp_mod, "PP_predictions")