import os
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.metrics import log_loss, roc_auc_score, roc_curve

from .cleaning import get_clean_data

def load_model():
    mod = xgb.XGBClassifier()
    mod.load_model(os.path.join(os.path.dirname(__file__), "xg_model.json"))
    return mod

def predict(mod):
    X_test, y_test = get_clean_data(20162017, 20162017)
    y_pred = mod.predict_proba(X_test)
    print(y_pred[:,1])
    X_test['isGoal'] = y_test
    X_test['xg'] = y_pred[:,1]

    X_test.to_pickle(os.path.join(os.path.dirname(__file__), "predictions.pkl"))

def model_importance(mod):
    xgb.plot_importance(mod)
    plt.show()

if __name__ == "__main__":
    mod = load_model()
    predict(mod)