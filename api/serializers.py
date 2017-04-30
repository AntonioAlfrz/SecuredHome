from rest_framework import serializers
from api.models import User, Log

class UserSerializer(serializers.ModelSerializer):

    logs = serializers.RelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('name','token','logs')

class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = ('date','command','user')