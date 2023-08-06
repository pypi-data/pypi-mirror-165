import inspect
import sys
import os
from pargv import parse_args


def magicli(exclude=['main'], help_message=True, glbls=None, argv=None):
    """
    Get all functions from calling file and interprets them as CLI commands.
    Parses command line arguments for function to call
    and calls it with all specified arguments.
    Displays a help message  and exits if the --help flag is set
    or if no callable function is found.
    Errors out with a TypeError if the specified arguments are invalid. 
    """
    glbls = glbls if glbls else inspect.currentframe().f_back.f_globals
    argv = argv if argv else sys.argv
    app_name, args, kwargs = format_args(argv)

    functions = [f for f in filter_functions(glbls) if f.__name__ not in exclude]

    if help_message and 'help' in kwargs:
        print_help_and_exit(app_name, functions)

    possible_commands = [f.__name__ for f in functions]
    function_name = None

    if len(args) and args[0] in possible_commands:
        function_name = args[0]
        args = args[1:]
    elif app_name in possible_commands:
        function_name = app_name
    else:
        print_help_and_exit(app_name, functions)
    
    function_to_call = glbls.get(function_name)
    
    try:
        function_to_call(*args, **kwargs)
    except TypeError as e:
        print_error(e)
        raise


def print_error(e):
    print('\x1b[91mError:\x1b[0m ', end='')
    print(e)


def format_args(argv):
    args, kwargs = parse_args(argv)
    app_name = os.path.basename(args[0])
    args = args[1:]
    return app_name, args, kwargs


def filter_functions(args):
    """
    Gets list of functions from the globals variable of a specific module (default: __main__).
    """
    return [v for k, v in args.items() if inspect.isfunction(v) and v.__module__ == args['__name__']]


def print_help_and_exit(app_name, functions):
    """
    Print the help message based on functions contained in the calling file.
    Exits after displaying the help message.
    """
    print('Usage:')
    for f in functions:
        words = []
        if app_name != f.__name__:
            words.append(app_name)
        words.append(f.__name__)
        specs = inspect.getfullargspec(f)
        words += ['--' + arg for arg in specs.args]
        print(' '*4 + ' '.join(words))
    exit()
