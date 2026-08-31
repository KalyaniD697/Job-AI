from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'


class JobSearchSerializer(serializers.Serializer):

    role = serializers.CharField(
        max_length=255
    )

    location = serializers.CharField(
        max_length=255
    )

    experience = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )