import xgboost as xgb
import pandas as pd
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from scipy.stats import uniform
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

    print("Loaded Data")

    xgclassifier_stage1 = xgb.XGBClassifier(objective='binary:logistic',
                                            verbosity = 1,
                                            tree_method = 'hist',
                                            n_jobs=None)

    distributions = {'eta': uniform(loc=0, scale=0.3)}
    clf_stage1 = RandomizedSearchCV(xgclassifier_stage1, distributions, random_state=5, scoring='neg_log_loss', n_jobs=1, verbose=3)
    clf_stage1.fit(X_train, y_train)
    eta = clf_stage1.best_params_['eta']

    print(f"Selected eta = {eta}")

    xgclassifier_stage2 = xgb.XGBClassifier(objective='binary:logistic',
                                            verbosity = 1,
                                            eta = eta,
                                            tree_method = 'hist',
                                            n_jobs=None)
    
    param_grid = {
        'gamma': [0, 0.01, 0.1],
        'max_depth': [3, 4, 5, 6],
        'subsample': [0.7, 0.9, 1],
        'min_child_weight': [0.5, 1, 1.5]
    }

    clf_stage2 = GridSearchCV(xgclassifier_stage2, param_grid, scoring='neg_log_loss', n_jobs=1, verbose=3)
    clf_stage2.fit(X_train, y_train)

    mod = clf_stage2.best_estimator_
    mod.save_model(os.path.join(os.path.dirname(__file__), "xg_model.json"))
    mod._Booster.dump_model(os.path.join(os.path.dirname(__file__), "xg_model_dump.json"))

    return mod

if __name__ == "__main__":
    train_model(load_from_file=False)