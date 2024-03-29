from rest_framework.renderers import JSONRenderer


class SnakeCaseJSONRenderer(JSONRenderer):
    format = "snake_case_json"
