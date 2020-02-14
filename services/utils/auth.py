from django.core.cache import cache
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from drowranger.utils.cache import create_key, CACHE_SERVICE_NAME, CACHE_SERVICE
from services.models import Service
from services.serializers import ServiceSerializer


class Authentication(BaseAuthentication):
    """用于用户登录验证"""

    def authenticate(self, request):
        service_name = request.headers['service']
        secret = request.headers['secret']

        if not service_name or not secret:
            raise exceptions.AuthenticationFailed('找不到服务')

        service_dict = cache.get(create_key(CACHE_SERVICE_NAME, service_name))
        if not service_dict:
            service = Service.objects.filter(service_name=service_name).first()
            if not service:
                raise exceptions.AuthenticationFailed('找不到服务')

            service_dict = ServiceSerializer(service).data
            cache.set(create_key(CACHE_SERVICE, service_dict['id']), service_dict)
            cache.set(create_key(CACHE_SERVICE_NAME, service_name), service_dict)

        if service_dict['secret'] != secret:
            raise exceptions.AuthenticationFailed('找不到服务')

        return service_dict, None

    def authenticate_header(self, request):
        pass
