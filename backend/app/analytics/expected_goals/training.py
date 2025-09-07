import os

import xgboost as xgb
from sklearn.model_selection import GridSearchCV

from .cleaning import load_seasons, clean_data, transform_data

def train_model(name, X_train, y_train, model_to_load=None):

    if model_to_load is not None:
        mod = xgb.XGBClassifier()
        mod.load_model(os.path.join(os.path.dirname(__file__), "models", model_to_load))
        mod.fit(X_train, y_train)
    else:
        xgclassifier = xgb.XGBClassifier(objective='binary:logistic',
                                        verbosity = 1,
                                        subsample = 0.9,
                                        tree_method = 'hist',
                                        n_jobs=None)

        param_grid = {
            'eta': [0.05, 0.08, 0.1, 0.2],
            'max_depth': [4, 5, 6, 7],
            'min_child_weight': [0.5, 1, 1.5]
        }

        clf = GridSearchCV(xgclassifier, param_grid, scoring='neg_log_loss', n_jobs=1, verbose=2)
        clf.fit(X_train, y_train)
        mod = clf.best_estimator_

    with open(os.path.join(os.path.dirname(__file__), "models", f"{name}_performance.txt"), "w") as f:
        f.write(f"{name} Stats: \n")
        f.write(f"Log-Loss (CV) = {clf.best_score_}\n")
        for param, value in mod.get_params().items():
            if param in ['eta', 'max_depth', 'min_child_weight']:
                f.write(f"{param}: {value}\n")
    
    mod.save_model(os.path.join(os.path.dirname(__file__), "models", f"{name}.json"))
    
    return mod

def load_model(name: str):
    mod = xgb.XGBClassifier()
    mod.load_model(os.path.join(os.path.dirname(__file__), "models", f"{name}.json"))
    return mod

if __name__ == "__main__":
    data = load_seasons(20142015, 20242025)
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