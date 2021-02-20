from rest_framework import serializers
from model.models import mUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = mUser
        fields = '__all__'

