import xgboost as xgb
import pandas as pd
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from scipy.stats import uniform
import os

from .cleaning import load_seasons, clean_data, transform_data

def train_model(name, X_train, y_train, model_to_load=None):

    if model_to_load is not None:
        mod = xgb.XGBClassifier()
        mod.load_model(os.path.join(os.path.dirname(__file__), "models", model_to_load))
        mod.fit(X_train, y_train)
    else:
        xgclassifier_stage1 = xgb.XGBClassifier(objective='binary:logistic',
                                                verbosity = 1,
                                                tree_method = 'hist',
                                                n_jobs=None)

        distributions = {'eta': uniform(loc=0, scale=0.3)}
        clf_stage1 = RandomizedSearchCV(xgclassifier_stage1, distributions, random_state=5, scoring='neg_log_loss', n_jobs=1, verbose=2)
        clf_stage1.fit(X_train, y_train)
        eta = clf_stage1.best_params_['eta']

        xgclassifier_stage2 = xgb.XGBClassifier(objective='binary:logistic',
                                                verbosity = 1,
                                                eta = eta,
                                                tree_method = 'hist',
                                                n_jobs=None)
        
        param_grid = {
            'gamma': [0, 0.01, 0.1],
            'max_depth': [3, 4, 5, 6],
            'subsample': [0.9, 1],
            'min_child_weight': [0.5, 1, 1.5]
        }

        clf_stage2 = GridSearchCV(xgclassifier_stage2, param_grid, scoring='neg_log_loss', n_jobs=1, verbose=2)
        clf_stage2.fit(X_train, y_train)
        mod = clf_stage2.best_estimator_

    with open(os.path.join(os.path.dirname(__file__), "models", f"{name}_performance.txt"), "w") as f:
        f.write(f"{name} Stats: \n")
        f.write(f"In-Sample Log-Loss (CV) = {clf_stage2.best_score_}\n")
        for param, value in mod.get_params().items():
            f.write(f"{param}: {value}\n")
    
    mod.save_model(os.path.join(os.path.dirname(__file__), "models", f"{name}.json"))
    
    return mod

if __name__ == "__main__":
    data = load_seasons(20102011, 20162017)
    es_data, pp_data, sh_data = clean_data(data)
    
    # Even Strength Model
    X_train_es, y_train_es, _ = transform_data(es_data, model='ES')
    train_model("ES_model", X_train_es, y_train_es)

    # Powerplay Model
    X_train_pp, y_train_pp, _ = transform_data(pp_data, model='PP')
    train_model("PP_model", X_train_pp, y_train_pp)

    # Shorthanded Model
    X_train_sh, y_train_sh, _ = transform_data(sh_data, model='SH')
    train_model("SH_model", X_train_sh, y_train_sh)