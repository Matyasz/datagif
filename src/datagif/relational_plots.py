from pathlib import Path
from typing import Dict

import imageio
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

from .utilities import get_imageio_defaults


valid_relational_plots = [
    'relplot', 'scatterplot', 'lineplot'
]


def _relational_plot(plot_type: str,
                     save_dir: str,
                     name: str,
                     data: pd.DataFrame,
                     x: str,
                     y: str,
                     t: str,
                     fix_x: bool = False,
                     fix_y: bool = False,
                     save_frames: bool = False,
                     plt_funcs: Dict[str, Dict] = None,
                     seaborn_args: Dict = None,
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
    plt_funcs : Dict[str, Dict], optional
        Any extra methods of the plot that should be called, the name of the
        method as a string for the key, and the value should be a dict
        containint the arguments to provide the method. And empty dict or
        None may be provided if no arguments are necessary.
    seaborn_args : Dict, optional
        Any extra arguments to pass to the seaborn plotting method to
        customize the plot. Defaults to None.
    imageio_args : Dict, optional
        Any extra arguments to pass to imageio to customize the gif.
        Defaults to None.
    """
    if plot_type not in valid_relational_plots:
        raise ValueError(
            f"Invalid relational plot. "
            f"Must be one of {valid_relational_plots}"
        )

    if seaborn_args is None:
        seaborn_args = {}

    if imageio_args is None:
        imageio_args = {}

    time_values = sorted(data[t].unique().tolist())

    plot = getattr(sns, plot_type)

    # Generate the individual frames of the .gif and save them
    saved_files = []
    for time in time_values:
        time_df = data.loc[data[t] == time]

        plot(x=x, y=y, data=time_df, **seaborn_args)

        if fix_x:
            plt.xlim(data[x].min(), data[x].max())
        if fix_y:
            plt.ylim(data[y].min(), data[y].max())

        filename = f"{save_dir}/{name}_{time}.png"
        saved_files.append(filename)

        # Call any extra desired plot methods
        for f in plt_funcs:
            plot_func = getattr(plt, f)

            if plt_funcs[f] is not None:
                plot_func(**plt_funcs[f])
            else:
                plot_func()

        # Save the image and close the plot
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


def relplot_gif(save_dir: str,
                name: str,
                data: pd.DataFrame,
                x: str,
                y: str,
                t: str,
                fix_x: bool = False,
                fix_y: bool = False,
                save_frames: bool = False,
                plt_funcs: Dict[str, Dict] = None,
                seaborn_args: Dict = None,
                imageio_args: Dict = None):
    """
    The user-exposed method for making animated gifs of seaborn relplots.

    Arguments
    ---------
    See the descriptions in the _relational_plots method.

    """
    _relational_plot(plot_type='relplot',
                     save_dir=save_dir,
                     name=name,
                     data=data,
                     x=x,
                     y=y,
                     t=t,
                     fix_x=fix_x,
                     fix_y=fix_y,
                     save_frames=save_frames,
                     plt_funcs=plt_funcs,
                     seaborn_args=seaborn_args,
                     imageio_args=imageio_args)


def scatterplot_gif(save_dir: str,
                    name: str,
                    data: pd.DataFrame,
                    x: str,
                    y: str,
                    t: str,
                    fix_x: bool = False,
                    fix_y: bool = False,
                    save_frames: bool = False,
                    plt_funcs: Dict[str, Dict] = None,
                    seaborn_args: Dict = None,
                    imageio_args: Dict = None):
    """
    The user-exposed method for making animated gifs of seaborn scatterplots.


    Arguments
    ---------
    See the descriptions in the _relational_plots method.

    """
    _relational_plot(plot_type='scatterplot',
                     save_dir=save_dir,
                     name=name,
                     data=data,
                     x=x,
                     y=y,
                     t=t,
                     fix_x=fix_x,
                     fix_y=fix_y,
                     save_frames=save_frames,
                     plt_funcs=plt_funcs,
                     seaborn_args=seaborn_args,
                     imageio_args=imageio_args)


def lineplot_gif(save_dir: str,
                 name: str,
                 data: pd.DataFrame,
                 x: str,
                 y: str,
                 t: str,
                 fix_x: bool = False,
                 fix_y: bool = False,
                 save_frames: bool = False,
                 plt_funcs: Dict[str, Dict] = None,
                 seaborn_args: Dict = None,
                 imageio_args: Dict = None):
    """
    The user-exposed method for making animated gifs of seaborn lineplots.


    Arguments
    ---------
    See the descriptions in the _relational_plots method.

    """
    _relational_plot(plot_type='lineplot',
                     save_dir=save_dir,
                     name=name,
                     data=data,
                     x=x,
                     y=y,
                     t=t,
                     fix_x=fix_x,
                     fix_y=fix_y,
                     save_frames=save_frames,
                     plt_funcs=plt_funcs,
                     seaborn_args=seaborn_args,
                     imageio_args=imageio_args)
