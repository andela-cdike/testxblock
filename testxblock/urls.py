from django.conf.urls import url

from .views import QuoteView


app_name = 'testxblock'


urlpatterns = [
    url(r'^quotes/', QuoteView.as_view(), name='quote_view'),
]
