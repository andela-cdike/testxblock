from __future__ import unicode_literals

import collections
import re
import requests
import HTMLParser

from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class QuoteView(APIView):

    def get(self, request, format=None):
        """Returns quotes from a third party service"""
        api_endpoint = (
            'https://quotesondesign.com/wp-json/posts?'
            'filter[orderby]=rand&filter[posts_per_page]=5'
        )
        resp = requests.get(api_endpoint)
        if resp.status_code == 200:
            quotes = sanitize_quotes(resp.json())
            data = {
                'msg': 'Welcome to my test endpoint. Enjoy these quotes.',
                'quotes': quotes
            }
            return Response(quotes, status=200)
        return Response('Oops, something went wrong! Try again', status=500)


def sanitize_quotes(quotes):
    """
    Returns a list of quotes that in the desired format

    :param quotes: a list of dictionaries
    :return: a list of dictionaries
    """
    return [
        collections.OrderedDict([
            ('s/n', idx),
            ('id', quote['ID']),
            ('content', escape_html_entity(
                remove_html_tags(
                    quote['content']
            )).strip('\n ')),
            ('link', quote['link']),
            ('title', quote['title']),
            ('source', extract_url_from_anchor_tag(
                quote.get('custom_meta', {}).get('Source', '')))
        ]) for idx, quote in enumerate(quotes, 1)
    ]


def remove_html_tags(text):
    """Removes leading and trailing HTML tags from supplied text
    and returns cleaned text

    :param text: string
    :returns: string
    """
    tag_pattern = re.compile(r'<[^>]+>')
    return tag_pattern.sub('', text)


def escape_html_entity(text):
    """Converts html entity codes to their unicode equivalents"""
    parser = HTMLParser.HTMLParser()
    return parser.unescape(text)


def extract_url_from_anchor_tag(text):
    """Extracts url from the href attribute in any anchor tag found in the
    supplied text

    :param text: string
    :return: a string of the url found
    """
    pattern = re.compile(r'(?<=href=").*?(?=")')
    matches = pattern.findall(text)
    return matches[0] if matches else ''
