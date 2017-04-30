from django.contrib import admin
from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
from api import urls, views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'logs', views.LogViewSet)

from rest_framework.authtoken import views
# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^test/', include(urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token/', views.obtain_auth_token),
]