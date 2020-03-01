from django.urls import re_path

from .views import UserList, UserDetail, EnrolmentRequestList, EnrolmentRequestDetail


urlpatterns = [
    re_path("^user/$", UserList.as_view(), name='user.list_view'),
    re_path("^user/(?P<slug>[\w\d-]+)/(?P<pk>[\w\d-]+)/$", UserDetail.as_view(), name='user.detail_view'),

    re_path("^enrolmentrequest/$", EnrolmentRequestList.as_view(), name='enrolmentrequest.list_view'),
    re_path("^enrolmentrequest/(?P<slug>[\w\d-]+)/(?P<pk>[\w\d-]+)/$", EnrolmentRequestDetail.as_view(),
            name='enrolmentrequest.detail_view')
]
