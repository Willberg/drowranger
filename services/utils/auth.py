from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from drowranger.settings import DROWRANGER_SERIVCE_NAME, DROWRANGER_SERVICE_SECRET


class Authentication(BaseAuthentication):
    """用于用户登录验证"""

    def authenticate(self, request):
        service_name = request.headers['service']
        secret = request.headers['secret']

        if not service_name or not secret:
            raise exceptions.AuthenticationFailed('找不到服务')

        if service_name != DROWRANGER_SERIVCE_NAME or secret != DROWRANGER_SERVICE_SECRET:
            raise exceptions.AuthenticationFailed('找不到服务')

        service_dict = {
            "service_name": service_name,
            "secret": secret
        }

        return service_dict, None

    def authenticate_header(self, request):
        pass
