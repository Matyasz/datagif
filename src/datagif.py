import seaborn as sns
import pandas as pd
import imageio

import matplotlib.pyplot as plt

sns.set_style(style="darkgrid")


def make_gif(save_dir: str, x: str, y: str, t: str, data,
             fix_y: bool = False, fix_x: bool = False,
             seaborn_args: dict = None, imageio_args: dict = None):
    """ooh if x is the same as t. then make sure to fill full plot and only 
    add new data as you go, so they don't need to super duplicate their data

    Args:
        path (str): [description]
        x (str): [description]
        y (str): [description]
        t (str): [description]
        data ([type]): [description]
        fix_y (bool, optional): [description]. Defaults to False.
        fix_x (bool, optional): [description]. Defaults to False.
        seaborn_args (dict, optional): [description]. Defaults to None.
        imageio_args (dict, optional): [description]. Defaults to None.
    """

    if seaborn_args is None:
        seaborn_args = {}

    if imageio_args is None:
        imageio_args = {}

    time_values = sorted(data[t].unique().tolist())

    for time in time_values:
        time_df = data.loc[data[t] == time]

        plot_args = {
            'x': x,
            'y': y,
            'data': time_df,
            **seaborn_args
        }

        # sns.lmplot(**plot_args)
        sns.relplot(**plot_args)

        if fix_x:
            plt.xlim(data[x].min(), data[x].max())
        if fix_y:
            plt.ylim(data[y].min(), data[y].max())

        plt.savefig(save_dir + f'{time}.png')

    # plt.show()


def validate_inputs():
    pass
