import os
import pickle

with open(os.path.join(os.path.dirname(__file__), "xgmodel.pkl"), 'rb') as f:
    mod = pickle.load(f)

print(mod.best_params_)