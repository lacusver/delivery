import json
from django.conf import settings
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from djangorestframework_camel_case.util import underscoreize
from utils.renderers.camel_case import CamelCaseJSONRenderer


class CamelCaseJSONParser(JSONParser):
    renderer_class = CamelCaseJSONRenderer

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            data = stream.read().decode(encoding)
            return underscoreize(json.loads(data))
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % exc)
