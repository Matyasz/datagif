def get_imageio_defaults(io_args):
    if 'duration' not in io_args:
        io_args['duration'] = 0.5
    if 'mode' not in io_args:
        io_args['mode'] = 'I'

    return io_args
