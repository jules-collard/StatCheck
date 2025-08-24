import os
import xgboost as xgb
import matplotlib.pyplot as plt

mod = xgb.XGBClassifier()
mod.load_model(os.path.join(os.path.dirname(__file__), "xg_model.json"))

xgb.plot_importance(mod)
plt.show()

# feature_importance = xg.get_booster().get_score(importance_type = 'weight')

# keys = list(feature_importance.keys())
# values = list(feature_importance.values())

# importance = pd.DataFrame(data = values, index=keys, columns=["score"]).sort_values(by="score", ascending=False)
# print(importance)