import logging
import time
import ntcore


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


def waitForNT() -> bool:
    inst = ntcore.NetworkTableInstance.getDefault()
    st = time.time()
    while time.time() - st < 10:
        if inst.isConnected():
            break
        time.sleep(0.1)
    else:
        return False
    table = inst.getTable('FMSInfo')
    st = time.time()
    while time.time() - st < 10:
        if table.getEntry('FMSControlData').getInteger(None) is not None and \
                table.getString('EventName', None) is not None and \
                table.getEntry('MatchType').getInteger(None) is not None and \
                table.getEntry('ReplayNumber').getInteger(None) is not None and \
                table.getEntry('MatchNumber').getInteger(None) is not None:
            break
        time.sleep(0.1)
    else:
        return False
    return True


def getMatchRepr():
    inst = ntcore.NetworkTableInstance.getDefault()
    table = inst.getTable('FMSInfo')

    match_type = int(table.getEntry('MatchType').getInteger(None))
    replay_number = table.getEntry('ReplayNumber').getInteger(None)
    match_number = table.getEntry('MatchNumber').getInteger(None)

    match_type_dict = {
        1: 'P',
        2: 'Q',
        3: 'E'
    }
    return f'{match_type_dict[match_type]}{match_number}_{replay_number}'


def getEventName():
    inst = ntcore.NetworkTableInstance.getDefault()
    table = inst.getTable('FMSInfo')
    name = table.getString('EventName', None)
    assert name is not None
    return name
