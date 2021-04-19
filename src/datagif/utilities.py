def get_imageio_defaults(io_args):
    if 'duration' not in io_args:
        io_args['duration'] = 0.5
    if 'mode' not in io_args:
        io_args['mode'] = 'I'

    return io_args


def validate_inputs():
    # if (
    #     isinstance(plot_types, list)
    #     and not all([isinstance(o, list) for o in [
    #         x, y, plt_funcs, seaborn_funcs, seaborn_args, imageio_args
    #     ]])
    # ):
    #     raise TypeError(
    #         'Arguments plot_types, x, y, plt_funcs, seaborn_funcs, '
    #         'seaborn_args, and imageio_args must either all be lists '
    #         'or all be single arguments'
    #     )
    pass
