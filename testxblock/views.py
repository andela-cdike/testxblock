import requests

from rest_framework.views import APIView
from rest_framework.response import Response


class QuoteView(APIView):

    def get(self, request, format=None):
        """Returns quotes from a third party service"""
        api_endpoint = (
            'https://quotesondesign.com/wp-json/posts?'
            'filter[orderby]=rand&filter[posts_per_page]=5'
        )
        resp = requests.get(api_endpoint)
        if resp.status_code == 200:
            quotes = [quote['content'] for quote in resp.json()]
            return Response(quotes, status=200)
        return Response('Oops, something went wrong! Try again', status=500)
