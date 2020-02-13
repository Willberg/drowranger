from django.core.cache import cache
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from drowranger.utils.cache import create_key, CACHE_SERVICE_NAME
from services.models import Service


class Authentication(BaseAuthentication):
    """用于用户登录验证"""

    def authenticate(self, request):
        service_name = request.headers['service']
        secret = request.headers['secret']

        if not service_name or not secret:
            raise exceptions.AuthenticationFailed('找不到服务')

        service_dict = cache.get(create_key(CACHE_SERVICE_NAME, service_name))
        if not service_dict:
            raise exceptions.AuthenticationFailed('找不到服务')

        service = Service()
        service.__dict__ = service_dict
        if service.secret != secret:
            raise exceptions.AuthenticationFailed('找不到服务')

        return service, None

    def authenticate_header(self, request):
        pass
