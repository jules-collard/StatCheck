from hockey_rink import NHLRink
import matplotlib.pyplot as plt
import pandas as pd
import os

predictions = pd.read_pickle(os.path.join(os.path.dirname(__file__), "predictions.pkl"))

rink = NHLRink(net={"visible": False})

common_params = {
    'x': 'xStd',
    'y': 'yStd',
    'values': 'xg',
    'data': predictions,
    'draw_kw': {'display_range': 'ozone', 'rotation': 270}
}

def plot_hexbin(ax):
    rink.hexbin(
        gridsize=(14, 9),
        extent=(25, 100, -42.5, 42.5),
        vmax=0.25,
        ax=ax,
        cmap='magma',
        **common_params,
    )

    min_color = plt.get_cmap("viridis")(0)

    half_length = 200 / 2
    half_width = 83 / 2

    rink.plot_fn(
        ax.fill,

        # Filling the entire rink for simplicity.
        x=[-half_length, half_length, half_length, -half_length],
        y=[-half_width, -half_width, half_width, half_width],

        color=min_color,
        zorder=2.5,

        # Matplotlib doesn't allow x and y to be passed as keyword parameters.
        # We get around this by telling plot_fn that they're positional
        # arguments.
        position_args=["x", "y"],
    )

def plot_contourf(ax):
    rink.contourf(
        nbins=8,
        levels=30,
        plot_range="ozone",
        cmap="bwr",
        ax=ax,
        **common_params,
    )

fig, axs = plt.subplots(figsize=(12,4))
plot_hexbin(axs)

plt.show()