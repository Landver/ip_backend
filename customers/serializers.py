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
        exclude = ['password']


class CreateUserSerializer(BaseSerializer):
    def create(self, validated_data):
        '''customized original function to set_password as hashed password'''
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['password', 'username', 'first_name', 'last_name', 'email', 'terms_confirmation']


class EnrolmentRequestSerializer(BaseSerializer):
    class Meta:
        model = EnrolmentRequest
        fields = '__all__'


class CreateEnrolmentRequestSerializer(BaseSerializer):
    class Meta:
        model = EnrolmentRequest
        exclude = ['user', 'review_pending', 'approved', 'email_confirmed', 'phone_confirmed', 'terms_confirmation']
