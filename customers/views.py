import re

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import FieldError, ValidationError

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    UserSerializer, CreateUserSerializer, EnrolmentRequestSerializer, CreateEnrolmentRequestSerializer
)
from .models import User, EnrolmentRequest


class UserList(ListCreateAPIView):
    def get_serializer_class(self):
        """default DRF method, little bit customized to return different serializers"""
        if self.request.method == 'POST':
            return CreateUserSerializer
        else:
            return super().get_serializer_class()

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        data = request.data

        if 'create_by_enrolmentrequest' in request.GET:
            obj = EnrolmentRequest.objects.get(id=request.GET['create_by_enrolmentrequest'])
            return(Response({"enrolmentrequest": EnrolmentRequestSerializer(obj).data}, status=status.HTTP_200_OK))

        if 'terms_confirmation' not in data or not data['terms_confirmation']:
            return(Response({"terms_confirmation": "terms need to be confirmed"}, status=status.HTTP_400_BAD_REQUEST))

        return self.list(request, *args, **kwargs)


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EnrolmentRequestList(ListCreateAPIView):
    queryset = EnrolmentRequest.objects.all()
    serializer_class = EnrolmentRequestSerializer
    filterset_fields = ['review_pending']

    def get_serializer_class(self):
        """default DRF method, little bit customized to return different serializers"""
        if self.request.method == 'POST':
            return CreateEnrolmentRequestSerializer
        else:
            return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save()

        obj = serializer.instance
        token = PasswordResetTokenGenerator()

        url = f'{settings.FRONTEND_URL}{obj.get_absolute_url()}'

        # Send confirmation to specified email.
        # TODO: Admin user need to be replaced, because it is security breach
        mail = (
            f"Mail confirmation",
            f"""
                Enrolment Request {obj.name} had been created. It will be reviewed within 3 days.
                Please click on the link below to confirm your email address:
                {url}?email-confirmation&token={token.make_token(User.objects.get(name='admin'))}
            """,
            "do_not_reply@ipfinity.project.corpberry.com",
            [f"{obj.email}"]
        )

        send_mail(*mail)

    def post(self, request, *args, **kwargs):
        data = request.data

        if 'terms_confirmation' not in data or not data['terms_confirmation']:
            return(Response({"terms_confirmation": "terms need to be confirmed"}, status=status.HTTP_400_BAD_REQUEST))

        return self.create(request, *args, **kwargs)


class EnrolmentRequestDetail(RetrieveUpdateDestroyAPIView):
    queryset = EnrolmentRequest.objects.all()
    serializer_class = EnrolmentRequestSerializer

    def perform_update(self, serializer):
        serializer.save()
        obj = serializer.instance
        data = self.request.data

        if 'approved' in data:
            if data['approved']:
                reply = f'''
                         Enrolment Request {obj.name} had been approved. You can registrate account by following URL:
                         {settings.FRONTEND_URL}/customers/user/?create_by_enrolmentrequest={obj.id}
                         '''
            else:
                reply = f'Enrolment Request {obj.name} had been declined'

            mail = (
                f"Enrolment Request status",
                reply,
                "do_not_reply@ipfinity.project.corpberry.com",
                [f"{obj.email}"]
            )

            send_mail(*mail)

    def check_token_and_confirm_email(self):
        kwargs = {"pk": self.kwargs["pk"]}

        token = PasswordResetTokenGenerator()
        enrolmentrequest = self.queryset.get(**kwargs)
        user = User.objects.get(name='admin')

        if token.check_token(user, self.request.GET['token']):
            enrolmentrequest.email_confirmed = True
            enrolmentrequest.save(update_fields=['email_confirmed'])
            return Response({'message': 'email had been confirmed'})

    def get(self, request, *args, **kwargs):
        if 'token' in request.GET and 'email-confirmation' in request.GET:
            return self.check_token_and_confirm_email()

        return super().get(request, *args, **kwargs)
