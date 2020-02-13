import time

from django.db import models


class Service(models.Model):
    STATUS_TYPE = (
        (1, '正常'),
        (2, '不可用'),
    )

    service_name = models.CharField(max_length=128, unique=True)
    domain = models.CharField(max_length=128)
    port = models.IntegerField()
    meta = models.CharField(max_length=512)
    secret = models.CharField(max_length=64)
    status = models.IntegerField(choices=STATUS_TYPE)
    create_time = models.BigIntegerField(default=int(round(time.time() * 1000)))
    update_time = models.BigIntegerField(default=int(round(time.time() * 1000)))
