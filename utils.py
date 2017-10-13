import time
import parky

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


def get_current_timestamp():
    cursor = parky.DbCursor()
    command = """SELECT blocks."timestamp" 
                 FROM blocks 
                 ORDER BY blocks."timestamp" DESC
                 LIMIT 1"""
    cursor.execute(command)
    return cursor.fetchone()[0]
