from django.conf.urls import url

from .views import TestView


# app_name = 'gk_api_testxblock'


urlpatterns = [
    url(r'^testxblock$', TestView.as_view(), name='test_view'),
]
