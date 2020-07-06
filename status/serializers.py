from rest_framework import serializers
from .models import StatusInput, AllStatusInput


class StatusInputSerializer(serializers.ModelSerializer):
    """
    Validate incoming status for rest_framework ajax transport
    """

    class Meta:
        model = StatusInput
        fields = '__all__'


class AllStatusInputSerializer(serializers.ModelSerializer):
    """
    Validate incoming request for all statuses for rest_framework ajax transport
    """

    class Meta:
        model = StatusInput
        fields = '__all__'


class AllStatusOutputSerializer(serializers.ModelSerializer):
    """
    package up all statuses for rest_framework ajax transport
    """

    class Meta:
        model = StatusInput
        fields = '__all__'
