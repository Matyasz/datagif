from pathlib import Path
from typing import Dict

import imageio
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

# sns.set_style(style="darkgrid")


def make_gif(save_dir: str,
             name: str,
             data: pd.DataFrame,
             x: str,
             y: str,
             t: str,
             fix_x: bool = False,
             fix_y: bool = False,
             save_frames: bool = False,
             seaborn_args: Dict = None,
             imageio_args: Dict = None):
    """ooh if x is the same as t. then make sure to fill full plot and only
    add new data as you go, so they don't need to super duplicate their data

    Arguments
    ---------
    save_dir : str
        Directory in which to store outputs.
    name : str
        The name for the output file.
    data : DataFrame
        A pandas DataFrame containing the data to be plotted.
    x : str
        The name of the column in `data` to be plotted on the x-axis.
        Identical to the x argument in the seaborn plotting method.
    y : str
        The name of the column in `data` to be plotted on the y-axis
        Identical to the y argument in the seaborn plotting method.
    t : str
        The name of the column in `data` to be used as the time dimension,
        i.e. will be fixed per plot/frame, and change in time with the gif.
    fix_x : bool, optional
        Whether or to allow the range of the x-axis to change with each
        frame of the gif. Defaults to False.
    fix_y : bool, optional
        Whether or to allow the range of the y-axis to change with each
        frame of the gif. Defaults to False.
    save_frames : bool
        Whether or not to save the individual frames of the .gif in
        addition to the .gif itself.
    seaborn_args : Dict, optional
        Any extra arguments to pass to the seaborn plotting method to
        customize the plot. Defaults to None.
    imageio_args : Dict, optional
        Any extra arguments to pass to imageio to customize the gif.
        Defaults to None.
    """

    if seaborn_args is None:
        seaborn_args = {}

    if imageio_args is None:
        imageio_args = {}

    time_values = sorted(data[t].unique().tolist())

    # Generate the individual frames of the .gif and save them
    saved_files = []
    for time in time_values:
        time_df = data.loc[data[t] == time]

        # plot_args = {
        #     'x': x,
        #     'y': y,
        #     'data': time_df,
        #     **seaborn_args
        # }

        # sns.lmplot(**plot_args)
        sns.relplot(x=x, y=y, data=time_df, **seaborn_args)

        if fix_x:
            plt.xlim(data[x].min(), data[x].max())
        if fix_y:
            plt.ylim(data[y].min(), data[y].max())

        filename = f"{save_dir}/{name}_{time}.png"
        saved_files.append(filename)

        plt.savefig(filename)

    # Prepare the imageio arguments with some defaults
    if 'duration' not in imageio_args:
        imageio_args['duration'] = 0.1
    if 'mode' not in imageio_args:
        imageio_args['mode'] = 'I'

    # Get the saved plots and combine them into a .gif
    with imageio.get_writer(
        f"{save_dir}/{name}.gif", **imageio_args
    ) as writer:

        for fn in saved_files:
            image = imageio.imread(fn)
            writer.append_data(image)

        writer.close()

    # Remove the intermediate files, unless the user wants to keep them
    if not save_frames:
        for sf in saved_files:
            Path(sf).unlink()


def validate_inputs():
    pass
