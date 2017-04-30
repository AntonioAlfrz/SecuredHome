from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api import views
from api.views import UserViewSet, LogViewSet

user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
log_list = LogViewSet.as_view({
    'get': 'list'
})
log_detail = LogViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([
    # http://localhost:8000/api/users/
    url(r'^users/', user_list),
    # Named capture group 'name' traga cualquier cosa
    url(r'^users/(?P<name>.+)$', user_detail),
    url(r'^logs/', log_list),
    url(r'^logs/(?P<name>.+)$', log_detail),
    url(r'^photo$', views.take_photo, name='take_photo'),
    url(r'^test$', views.test, name='test'),
    url(r'^list$', views.list, name='list'),
    url(r'^token$', views.token, name='token'),
    url(r'^refresh$', views.refresh, name='refresh'),
    # Default
    url(r'^', views.index, name='index'),
])