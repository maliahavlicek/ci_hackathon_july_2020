from accounts.models import Family
from users.serializers import UserSerializer
from rest_framework import serializers


class FamilySerializer(serializers.ModelSerializer):
    """
    Serialize Family Back so Status and Posts can be dynamically updated via ajax
    """
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Family
        fields = '__all__'
