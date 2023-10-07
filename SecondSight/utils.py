import logging
import time


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


def get8601date():
    now = time.localtime()
    return f'{now.tm_year}{now.tm_mon}{now.tm_mday if now.tm_mday > 9 else "0" + str(now.tm_mday)}{now.tm_hour if now.tm_hour > 9 else "0" + str(now.tm_hour)}{now.tm_min if now.tm_min > 9 else "0" + str(now.tm_min)}{now.tm_sec if now.tm_sec > 9 else "0" + str(now.tm_sec)}'
