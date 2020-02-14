from rest_framework import serializers

from services.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        # fields = '__all__'
        fields = (
            'id', 'service_name', 'domain', 'port', 'service_uri', 'meta', 'secret', 'status', 'create_time',
            'update_time')
