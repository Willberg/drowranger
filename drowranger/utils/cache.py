# service相关缓存
CACHE_SERVICE = 'drowranger_service'
CACHE_SERVICE_NAME = 'drowranger_service_name'


def create_key(scope, key):
    return scope + '_' + str(key)
