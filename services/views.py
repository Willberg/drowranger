import logging

from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView

from drowranger.utils import encrypt
from drowranger.utils.cache import create_key, CACHE_SERVICE
from drowranger.utils.errors import CODE_SYS_DB_ERROR, get_error_message, CODE_SYS_TIPS
from drowranger.utils.result import Result
from services.models import Service
from services.serializers import ServiceSerializer

log = logging.getLogger('django')


class ListView(APIView):
    @staticmethod
    def post(request):
        result = Result()
        service_id = request.POST.get('service_id')
        if not service_id:
            result.code = CODE_SYS_TIPS
            result.message = "service_id can't be empty"
            return JsonResponse(result.serializer())

        service_name = request.POST.get('service_name')
        domain = request.POST.get('domain')
        port = request.POST.get('port')
        meta = request.POST.get('meta')
        status = request.POST.get('status')

        service = Service()
        service.__dict__ = cache.get(create_key(CACHE_SERVICE, service_id))
        # 修改标记
        update_flag = 0
        if service_name and service.service_name != service_name:
            update_flag += 1
            service.service_name = service_name
        elif domain and service.domain != domain:
            update_flag += 1
            service.domain = domain
        elif port and service.port != int(port):
            update_flag += 1
            service.port = port
        elif meta and service.meta != meta:
            update_flag += 1
            service.meta = meta
        elif status and service.status != int(status):
            update_flag += 1
            service.status = status

        if update_flag == 0:
            result.code = CODE_SYS_TIPS
            result.message = "nothing to be updated"
            return JsonResponse(result.serializer())

        language = request.POST.get('language')
        language = language if not language else 'EN'

        try:
            with transaction.atomic():
                count = Service.objects.filter(id=service_id).update(service_name=service.service_name,
                                                                     domain=service.domain,
                                                                     port=service.port, meta=service.meta,
                                                                     status=service.status)

                service_dict = ServiceSerializer(service).data
                cache.set(create_key(CACHE_SERVICE, service.id), service_dict, timeout=None)
        except Exception as e:
            log.error(e)
            result.code = CODE_SYS_DB_ERROR
            result.message = get_error_message(result.code, language)

        result = Result()
        result.data = count
        return JsonResponse(result.serializer())

    @staticmethod
    def get(request):
        service_id = request.POST.get('service_id')
        result = Result()
        if not service_id:
            service_dict = cache.get(create_key(CACHE_SERVICE, service_id))
            result.data = service_dict
            return JsonResponse(result.serializer())

        service_list = Service.objects.all()
        service_dict_list = list()
        for service in service_list:
            s = ServiceSerializer(service).data
            service_dict_list.append(s)

        result.data = service_dict_list
        return JsonResponse(result.serializer())

    @staticmethod
    def put(request):
        service_name = request.POST.get('service_name')
        domain = request.POST.get('domain')
        port = request.POST.get('port')
        meta = request.POST.get('meta')
        status = request.POST.get('status')
        language = request.POST.get('language')
        language = language if not language else 'EN'

        # 访问秘钥
        secret = encrypt.digest_random()
        secret = encrypt.digest(secret)

        result = Result()
        try:
            with transaction.atomic():
                service = Service(service_name=service_name, domain=domain, port=port, meta=meta, secret=secret,
                                  status=status)
                service.save()

                service_dict = ServiceSerializer(service).data
                cache.set(create_key(CACHE_SERVICE, service.id), service_dict, timeout=None)
        except Exception as e:
            log.error(e)
            result.code = CODE_SYS_DB_ERROR
            result.message = get_error_message(result.code, language)

        result.data = service_dict
        return JsonResponse(result.serializer())

    @staticmethod
    def delete(request):
        service_id = request.POST.get('service_id')
        language = request.POST.get('language')
        language = language if not language else 'EN'

        result = Result()
        try:
            with transaction.atomic():
                Service.objects.filter(id=service_id).delete()

                cache.delete(create_key(CACHE_SERVICE, service_id))
        except Exception as e:
            log.error(e)
            result.code = CODE_SYS_DB_ERROR
            result.message = get_error_message(result.code, language)
        return JsonResponse(result.serializer())
