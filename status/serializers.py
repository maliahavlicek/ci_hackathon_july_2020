from rest_framework import serializers
from .models import StatusInput, AllStatusInput, Status
from users.models import User


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
        model = AllStatusInput
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    """
    Package up status for rest_framework ajax transport
    """

    class Meta:
        model = Status
        fields = ['mood', 'plans', 'help', 'updated_date']
