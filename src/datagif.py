from typing import Dict

import imageio
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

sns.set_style(style="darkgrid")


def make_gif(save_dir: str,
             x: str,
             y: str,
             t: str, data,
             fix_y: bool = False,
             fix_x: bool = False,
             seaborn_args: Dict = None,
             imageio_args: Dict = None):
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

    saved_files = []
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

        filename = save_dir + f'{time}.png'
        saved_files.append(filename)

        plt.savefig(filename)

    # plt.show()
    with imageio.get_writer(f"{save_dir}GIF.gif", mode='I', duration=0.1) as writer:
        for fn in saved_files:
            image = imageio.imread(fn)
            writer.append_data(image)

        writer.close()


def validate_inputs():
    pass
