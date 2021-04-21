import numpy as np
import pandas as pd
from pathlib import Path

from datagif import datagif

"""
Based on this example from the Seaborn documentation:
    https://seaborn.pydata.org/examples/layered_bivariate_plot.html
"""

dfs = []
t = 20

for times in range(1, t + 1):
    # Simulate data from a bivariate Gaussian
    n = 5000
    mean = [12 * np.sin(times / (2 * t)), 12 * np.cos(times / (2 * t))]
    cov = [(2, .4), (.4, .2)]
    rng = np.random.RandomState(times)
    x, y = rng.multivariate_normal(mean, cov, n).T

    dfs.append(pd.DataFrame({
        'time': [times for _ in range(len(x))],
        'longitude': x,
        'latitude': y
    }))

df = pd.concat(dfs, ignore_index=True)

datagif(
    plots=['scatterplot', 'histplot', 'kdeplot'],
    save_dir=str(Path(__file__).parent / 'plots'),
    name='gaussian_scatter',
    data=df,
    x=['longitude', 'longitude', 'longitude'],
    y=['latitude', 'latitude', 'latitude'],
    t='time',
    fix_x=True,
    fix_y=True,
    plt_funcs={
        'tight_layout': None,
        'subplots': {
            'figsize': (6, 6)
        },
        'title': 'Hurricane Trajectory'
    },
    seaborn_funcs={
        'set_theme': {'style': 'dark'}
    },
    seaborn_args=[
        {
            's': 5,
            'color': '0.15',
            'clip_on': False
        },
        {
            'bins': 50,
            'pthresh': .1,
            'cmap': "mako"
        },
        {
            'levels': 5,
            'color': "w",
            'linewidths': 1
        }
    ],
    imageio_args={
        'duration': 0.3
    }
)
