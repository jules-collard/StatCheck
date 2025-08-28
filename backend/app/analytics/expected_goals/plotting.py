from hockey_rink import NHLRink
import matplotlib.pyplot as plt
import xgboost as xgb
import pandas as pd
import seaborn as sns
import os

from .testing import load_model

rink = NHLRink(net={"visible": False})

common_params = {
    'x': 'xStd',
    'y': 'yStd',
    'values': 'xg',
    "draw_kw": {"display_range": "ozone", "rotation": 270}
}

def plot_hexbin(ax, data, cmap):
    rink.hexbin(
        gridsize=(14, 9),
        extent=(25, 100, -42.5, 42.5),
        vmax=0.25,
        ax=ax,
        data=data,
        cmap=cmap,
        **common_params,
    )

    min_color = plt.get_cmap(cmap)(0)

    half_length = 200 / 2
    half_width = 83 / 2

    rink.plot_fn(
        ax.fill,
        x=[-half_length, half_length, half_length, -half_length],
        y=[-half_width, -half_width, half_width, half_width],
        color=min_color,
        zorder=2.5,
        position_args=["x", "y"],
    )

def plot_shot_density(ax, data, cmap):
    rink.plot_fn(
        sns.kdeplot,
        x='xStd', y='yStd',
        cmap=cmap, fill=True, alpha=0.8,
        levels=20,
        data=data,
        ax=ax,
        draw_kw={"display_range": "ozone", "rotation": 270}
    )

def plot_shot_locations(es_predictions, pp_predictions, cmap='plasma'):
    fig, axs = plt.subplots(1,2)
    plot_shot_density(axs[0], es_predictions, cmap=cmap)
    axs[0].set_title('Even Strength')
    plot_shot_density(axs[1], pp_predictions, cmap=cmap)
    axs[1].set_title('Powerplay')

    fig.suptitle("Shot Locations", fontweight='bold', fontsize=16)

    plt.show()

def plot_heatmaps(es_predictions, pp_predictions, cmap='plasma'):
    fig, axs = plt.subplots(1, 2)
    plot_hexbin(axs[0], es_predictions, cmap=cmap)
    axs[0].set_title('Even Strength')
    plot_hexbin(axs[1], pp_predictions, cmap=cmap)
    axs[1].set_title('Powerplay')

    fig.suptitle("xG by Location", fontweight="bold", fontsize=16)

    plt.show()

def plot_feature_importance(name: str):
    mod = load_model(name)
    xgb.plot_importance(mod)

if __name__ == "__main__":
    es_predictions = pd.read_pickle(os.path.join(os.path.dirname(__file__), "models", "ES_predictions.pkl"))
    pp_predictions = pd.read_pickle(os.path.join(os.path.dirname(__file__), "models", "PP_predictions.pkl"))

    plot_shot_locations(es_predictions, pp_predictions)
