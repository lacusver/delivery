from djangorestframework_camel_case.util import camelize
from rest_framework.renderers import JSONRenderer


class CamelCaseJSONRenderer(JSONRenderer):
    format = "camel_case_json"

    def render(self, data, *args, **kwargs):
        return super(CamelCaseJSONRenderer, self).render(camelize(data), *args, **kwargs)
