import numpy as np
import pandas as pd

from pathlib import Path

from datagif import make_gif


def test_make_gif():
    dfs = []
    n = 20
    t = 3

    for times in range(1, t + 1):
        data = [5 + (times * i) + (2 * np.random.normal()) for i in range(n)]
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

    make_gif(
        save_dir=str(Path(__file__).parent / 'assets'),
        name='test',
        data=df,
        x='xval', y='yval', t='time',
        fix_x=True, fix_y=True
    )


if __name__ == "__main__":
    test_make_gif()
