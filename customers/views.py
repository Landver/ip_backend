from .models import User, EnrolmentRequest
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import UserSerializer, EnrolmentRequestSerializer


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EnrolmentRequestList(ListCreateAPIView):
    queryset = EnrolmentRequest.objects.all()
    serializer_class = EnrolmentRequestSerializer


class EnrolmentRequestDetail(RetrieveUpdateDestroyAPIView):
    queryset = EnrolmentRequest.objects.all()
    serializer_class = EnrolmentRequestSerializer
