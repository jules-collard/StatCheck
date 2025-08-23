import xgboost as xgb
import pandas as pd
import pickle
from sklearn.model_selection import GridSearchCV
import os

from .cleaning import get_clean_data

def train_model(load_from_file=True):
    if load_from_file:
        X_train = pd.read_pickle(os.path.join(os.path.dirname(__file__), "X_train.pkl"))
        y_train = pd.read_pickle(os.path.join(os.path.dirname(__file__), "y_train.pkl"))
    else:
        X_train, y_train = get_clean_data(20102011, 20152016)
        X_train.to_pickle(os.path.join(os.path.dirname(__file__), "X_train.pkl"))
        y_train.to_pickle(os.path.join(os.path.dirname(__file__), "y_train.pkl"))

    param_grid = {
        'eta': [0.2, 0.3, 0.4],
        'gamma': [0, 0.01, 0.1],
        'max_depth': [3, 6, 8, 10]
    }

    xgclassifier = xgb.XGBClassifier(objective='binary:logistic',
                                    verbosity = 1,
                                    tree_method = 'hist',
                                    n_jobs=None)
    mod = GridSearchCV(xgclassifier, param_grid, scoring='neg_log_loss', n_jobs=1, verbose=3)
    mod.fit(X_train, y_train)

    with open(os.path.join(os.path.dirname(__file__), "xgmodel.pkl"), 'wb') as f:
        pickle.dump(mod, f)

if __name__ == "__main__":
    train_model(load_from_file=False)