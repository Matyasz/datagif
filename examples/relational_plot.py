import numpy as np
import pandas as pd

from pathlib import Path

from datagif import (
    relplot_gif, scatterplot_gif, lineplot_gif
)


dfs = []
n = 20
t = 15

for times in range(1, t + 1):
    data = [5 + (times * i) + (15 * np.random.normal()) for i in range(n)]
    xval = [i for i in range(n)]
    time = [times for _ in range(n)]

    dfs.append(
        pd.DataFrame({
            'time': time,
            'xval': xval,
            'yval': data
        })
    )

df = pd.concat(dfs, ignore_index=True)

relplot_gif(
    save_dir=str(Path(__file__).parent / 'plots'),
    name='relplot_test',
    data=df,
    x='xval',
    y='yval',
    t='time',
    fix_x=True,
    fix_y=True,
    plt_funcs={
        'tight_layout': None
    },
    seaborn_args={'clip_on': False},
    imageio_args={'duration': 0.1}
)

scatterplot_gif(
    save_dir=str(Path(__file__).parent / 'plots'),
    name='scatterplot_test',
    data=df,
    x='xval',
    y='yval',
    t='time',
    fix_x=True,
    fix_y=True,
    plt_funcs={
        'tight_layout': None
    },
    seaborn_args={'clip_on': False},
    imageio_args={'duration': 0.1}
)

lineplot_gif(
    save_dir=str(Path(__file__).parent / 'plots'),
    name='lineplot_test',
    data=df,
    x='xval',
    y='yval',
    t='time',
    fix_x=True,
    fix_y=True,
    plt_funcs={
        'tight_layout': None
    },
    seaborn_args={},
    imageio_args={'duration': 0.1}
)
