from .models import User
from status.serializers import StatusSerializer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Package up User for rest_framework ajax transport
    """
    status = StatusSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'status']
