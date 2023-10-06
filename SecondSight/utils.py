import logging


def LogMe(func):
    def inner(*args, **kwargs):
        msg = f'{func.__module__}.{func.__qualname__}('
        logging.debug(f'Entered {msg})')
        for arg in args:
            msg += f'{repr(arg)}, '
        for name, kwarg in kwargs.items():
            msg += f'{name}= {kwarg}, '
        msg = msg.strip(', ')
        msg += ')'
        fn_out = func(*args, **kwargs)
        msg += f': {repr(fn_out)}'
        logging.debug(msg)
        return fn_out
    return inner
