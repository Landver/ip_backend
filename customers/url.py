from django.urls import re_path

from .views import UserList, UserDetail, EnrolmentRequestList, EnrolmentRequestDetail


urlpatterns = [
    re_path(f"^user/$", UserList.as_view(), name=f'user.list_view'),
    re_path(f"^user/(?P<slug>[\w\d-]+)/(?P<pk>[\w\d-]+)/$", UserDetail.as_view(), name=f'user.detail_view'),

    re_path(f"^enrolmentrequest/$", EnrolmentRequestList.as_view(), name=f'enrolmentrequest.list_view'),
    re_path(f"^enrolmentrequest/(?P<slug>[\w\d-]+)/(?P<pk>[\w\d-]+)/$", EnrolmentRequestDetail.as_view(),
            name=f'enrolmentrequest.detail_view')
]
