# service相关缓存
CACHE_SERVICE = 'drowranger_service'


def create_key(scope, key):
    return scope + '_' + str(key)
