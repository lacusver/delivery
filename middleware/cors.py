import logging

from django.conf import settings
from django.http import HttpResponse

request_logger = logging.getLogger("request")


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.META.get("HTTP_ORIGIN")
        has_access_control_request_method = (
            request.META.get("HTTP_ACCESS_CONTROL_REQUEST_METHOD") is not None
        )
        is_options = request.method == "OPTIONS"
        allowed_origin = origin in settings.ACCESS_CONTROL_ALLOW_ORIGIN
        is_pre_flight = (
            is_options
            and origin is not None
            and has_access_control_request_method
            and allowed_origin
        )
        response = (
            self.get_response(request)
            if not is_pre_flight
            else HttpResponse(status=200)
        )
        if settings.ACCESS_CONTROL_ALLOW_ORIGIN:
            if origin in settings.ACCESS_CONTROL_ALLOW_ORIGIN:
                response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = (
                "GET,PUT,POST,PATCH,DELETE,OPTIONS"
            )
            response["Access-Control-Allow-Headers"] = (
                "Content-Type, Authorization, traceparent, traceid, "
                "spanid, trace_id, span_id"
            )

        return response
