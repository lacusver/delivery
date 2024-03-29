from rest_framework.parsers import JSONParser
from utils.renderers.snake_case import SnakeCaseJSONRenderer


class SnakeCaseJSONParser(JSONParser):
    renderer_class = SnakeCaseJSONRenderer
