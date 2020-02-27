from rest_framework import serializers

from .models import User, EnrolmentRequest


class BaseSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        '''generate complete url of an object, like app_label/model_name/slug/id/'''
        return f"{obj.get_absolute_url()}"


class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EnrolmentRequestSerializer(BaseSerializer):
    class Meta:
        model = EnrolmentRequest
        fields = '__all__'
