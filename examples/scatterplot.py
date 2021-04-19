import numpy as np
import pandas as pd
from pathlib import Path

from datagif import datagif

# sns.set_theme(style="dark")  ## TODO ADD A SNS_FUNCS ARGUMENT

dfs = []
n = 20
t = 30

for times in range(1, t + 1):
    # Simulate data from a bivariate Gaussian
    n = 1000
    mean = [0, 0]
    cov = [(2, .4), (.4, .2)]
    rng = np.random.RandomState(times)
    x, y = rng.multivariate_normal(mean, cov, n).T

    dfs.append(pd.DataFrame({
        'time': [times for _ in range(len(x))],
        'xval': x,
        'yval': y
    }))

df = pd.concat(dfs, ignore_index=True)

# Draw a combo histogram and scatterplot with density contours
# f, ax = plt.subplots(figsize=(6, 6))
# sns.scatterplot(x=x, y=y, s=5, color=".15")
# sns.histplot(x=x, y=y, bins=50, pthresh=.1, cmap="mako")
# sns.kdeplot(x=x, y=y, levels=5, color="w", linewidths=1)

datagif(
    plots=['scatterplot', 'histplot', 'kdeplot'],
    save_dir=str(Path(__file__).parent / 'plots'),
    name='gaussian_scatter',
    data=df,
    x=['xval', 'xval', 'xval'],
    y=['yval', 'yval', 'yval'],
    t='time',
    fix_x=True,
    fix_y=True,
    plt_funcs={
        'tight_layout': None,
        'subplots': {
            'figsize': (6, 6)
        }
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
