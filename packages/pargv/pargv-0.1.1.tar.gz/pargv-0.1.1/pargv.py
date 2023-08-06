import sys


def parse_args(argv=None):
    """
    Returns a tuple of (args, kwargs) from a given list of command line arguments.
    Defaults to using `sys.argv`.
    """
    argv = argv if argv else sys.argv

    args = []
    for arg in argv:
        if arg.startswith('-'):
            break
        args.append(arg)
    argv = argv[len(args):]

    kwargs = {}
    values = []
    for arg in argv:
        if not arg.startswith('-'):
            values.append(arg)
        else:
            if len(values):
                kwargs[key] = values
                values = []
            key = arg[:2].lstrip('-') + arg[2:].replace('-', '_')
            if arg.startswith('--'):
                if '=' in arg:
                    key, value = key.split('=')
                    values.append(value)
                    kwargs[key] = values
                else:
                    kwargs[key] = True
            elif arg.startswith('-'):
                for k in key:
                    kwargs[k] = True
                key = arg[-1]
    if len(values):
        kwargs[key] = values
    return (args, kwargs)
