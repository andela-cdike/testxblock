import re
import requests

from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class QuoteView(APIView):

    renderer_classes = (BrowsableAPIRenderer,)

    def get(self, request, format=None):
        """Returns quotes from a third party service"""
        api_endpoint = (
            'https://quotesondesign.com/wp-json/posts?'
            'filter[orderby]=rand&filter[posts_per_page]=5'
        )
        resp = requests.get(api_endpoint)
        if resp.status_code == 200:
            quotes = [quote['content'].replace('\n', '') for quote in resp.json()]
            data = {
                'msg': 'Welcome to my test endpoint. Enjoy these quotes.',
                'quotes': quotes
            }
            return Response(data, status=200)
        return Response('Oops, something went wrong! Try again', status=500)
