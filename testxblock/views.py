import re
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
            quotes = [strip_html_tags(quote['content'])
                      for quote in resp.json()]
            data = {
                'msg': 'Welcome to my test endpoint. Enjoy these quotes.',
                'quotes': quotes
            }
            return Response(data, status=200)
        return Response('Oops, something went wrong! Try again', status=500)


def strip_html_tags(text):
    """Strips leading and trailing HTML tags from supplied text
    and returns cleaned text

    :param text: string
    :returns: string
    """
    tag_pattern = re.compile(r'<[^>]+>')
    return tag_pattern.sub('', text)
