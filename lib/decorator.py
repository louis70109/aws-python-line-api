from functools import wraps
from logging import Logger


def lambda_warm_up(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        source = args[0].get('source')
        if (source == 'serverless-plugin-warmup'):
            Logger.info('WarmUp - Lambda is warm!')
            return {}
        return func(*args, **kwargs)
    return wrapper
