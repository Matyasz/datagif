from pathlib import Path
from typing import Dict, List, Union

import imageio
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

from .utilities import get_imageio_defaults, validate_inputs


def datagif(plots: Union[List[str], str],
            save_dir: str,
            name: str,
            data: pd.DataFrame,
            x: Union[List[str], str],
            y: Union[List[str], str],
            t: str,
            fix_x: bool = False,
            fix_y: bool = False,
            save_frames: bool = False,
            tight_layout: bool = True,
            plt_funcs: Dict[str, Dict] = None,
            seaborn_funcs: Dict = None,
            seaborn_args: Union[List[Dict], Dict] = None,
            imageio_args: Dict = None):
    """
    This is the worker method for creating the relational plot gifs.

    Takes data in the form a pandas DataFrame, and turns the specified columns
    into a gif of a seaborn relplot using given plot arguments.

    Arguments
    ---------
    plot_type : str
        The plotting method from seaborn to use.
        Must be a valid relational plot.
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
    tight_layout : bool
        Whether or not to use the tight_layout method. This is highly
        recommended, as it prevents small difference between the individual
        plots that make up the gif leading to a much smoother animation.
        As such, it defaults to true for a better user experience.
    plt_funcs : Dict[str, Dict], optional
        Any extra methods of the plot that should be called, the name of the
        method as a string for the key, and the value should be a dict
        containint the arguments to provide the method. And empty dict or
        None may be provided if no arguments are necessary.
    seaborn_funcs : Dict, optional
        Any extra methods that should be called by the seaborn package,
        for example: sns.set_theme('dark')
    seaborn_args : Dict, optional
        Any extra arguments to pass to the seaborn plotting method to
        customize the plot. Defaults to None.
    imageio_args : Dict, optional
        Any extra arguments to pass to imageio to customize the gif.
        Defaults to None.
    """
    # Validate that the input dimensions are compatible
    validate_inputs()

    if seaborn_args is None:
        seaborn_args = {}

    if imageio_args is None:
        imageio_args = {}

    time_values = sorted(data[t].unique().tolist())

    if isinstance(plots, str):
        plots = [plots]

    saved_files = []

    # Call any extra desired seaborn methods
    for f in seaborn_funcs:
        seaborn_func = getattr(sns, f)

        if seaborn_funcs[f] is not None:
            seaborn_func(**seaborn_funcs[f])
        else:
            seaborn_func()

    for time in time_values:
        time_df = data.loc[data[t] == time]

        # Call any extra desired plot methods
        if tight_layout:
            plt.tight_layout()

        for f in plt_funcs:
            plot_func = getattr(plt, f)

            if plt_funcs[f] is not None:
                if isinstance(plt_funcs[f], dict) or \
                   isinstance(plt_funcs[f], list):
                    plot_func(**plt_funcs[f])
                else:
                    plot_func(plt_funcs[f])
            else:
                plot_func()

        # Loop over the plot and add one at a time
        for plot_num, p in enumerate(plots):
            plot = getattr(sns, p)
            plot(
                x=x[plot_num],
                y=y[plot_num],
                data=time_df,
                **(seaborn_args[plot_num])
            )

        if fix_x:
            plt.xlim(data[[*x]].to_numpy().min(), data[[*x]].to_numpy().max())
        if fix_y:
            plt.ylim(data[[*y]].to_numpy().min(), data[[*y]].to_numpy().max())

        # Save the image and close the plot
        filename = f"{save_dir}/{name}_{time}.png"
        saved_files.append(filename)

        plt.savefig(filename)
        plt.close()

    # Prepare the imageio arguments with some defaults
    imageio_args = get_imageio_defaults(imageio_args)

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
