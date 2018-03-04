from django.conf.urls import url
from rest_framework_jwt.views import verify_jwt_token
from . import views

urlpatterns = [
    url(r'^api/public$', views.public),
    url(r'^api/private$', views.private),
    url(r'^api/private-scoped$', views.private_scoped),
    url(r'^api/private-scoped-write$', views.private_scoped_write),
    url(r'^api/list-country$', views.CountryListAPIView.as_view(), name='list-api-view'),
    url(r'^api/verify-jwt-token$', verify_jwt_token),
]
