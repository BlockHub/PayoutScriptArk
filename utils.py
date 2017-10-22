import config
import time
import parky
import rotlog as rl

ARK = 100000000



class BlockIndexError(Exception):
    pass


class NameError(Exception):
    pass


class PayoutError(Exception):
    pass


def api_call(func, *args, **kwargs):
    result = None
    for i in range(15):
        if len(args):
            if kwargs:
                result = func(*args, **kwargs)
            else:
                result = func(*args)
        else:
            if kwargs:
                result = func(**kwargs)
            else:
                result = func()
        if result and 'success' in result and result['success']:
            return result
        time.sleep(5)
    return result
    # raise Exception(str(func) + ' failed 15 times')


def api_call_cached(func, *args, **kwargs):
    if not hasattr(api_call_cached, 'cache'):
        api_call_cached.cache = {}
    cache_key = '%s/%s/%s' % (str(func), str(args), str(kwargs))
    if cache_key not in api_call_cached.cache:
        api_call_cached.cache[cache_key] = api_call(func, *args, **kwargs)
    return api_call_cached.cache[cache_key]


def get_max_timestamp(cursor=None):
    # Fetch the max timestamp as it occurs in table blocks, or return
    # a previously cached value.

    if not cursor:
        cursor = parky.DbCursor()
        
    if not hasattr(get_max_timestamp, 'timestamp'):
        r = cursor.execute_and_fetchone(
            'SELECT MAX(timestamp) FROM blocks')
        if not r or not r[0]:
            raise utils.PayoutError('failed to get max timestamp from blocks: '
                                    + e)
        get_max_timestamp.timestamp = r[0]
    return get_max_timestamp.timestamp 

def timestamp(t = None, forfilename=False):
    """Returns a human-readable timestamp given a Unix timestamp 't' or
    for the current time. The Unix timestamp is the number of seconds since
    start of epoch (1970-01-01 00:00:00).

    When forfilename is True, then spaces and semicolons are replace with
    hyphens. The returned string is usable as a (part of a) filename. """

    datetimesep = ' '
    timesep     = ':'
    if forfilename:
        datetimesep = '-'
        timesep     = '-'

    return time.strftime('%Y-%m-%d' + datetimesep +
                         '%H' + timesep + '%M' + timesep + '%S',
                         time.localtime(t))

def arctimestamp(arct, forfilename=False):
    """Returns a human-readable timestamp given an Ark timestamp 'arct'.
    An Ark timestamp is the number of seconds since Genesis block,
    2017:03:21 15:55:44."""

    t = arct + time.mktime((2017, 3, 21, 15, 55, 44, 0, 0, 0))
    return '%d %s' % (arct, timestamp(t))

def setuplogging(progname):
    """ Set op the logging for rotlog, according to the values in config.py
    and for program 'progname'. Also log the run start. """
    rl.logfile(config.LOGGING['logfile'], maxsize=config.LOGGING['maxsize'],
               progname=progname)
    rl.verbose(config.LOGGING['verbosity'])
    rl.info('starting')
            
