from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.core.validators import URLValidator
from rest_framework import status


class ConsentURI(APIView):
    def post(self, request):
        base_uri = settings.OAUTH_BASE_URI
        redirect_uri = request.data.get('redirect_uri')
        client_id = settings.OAUTH_CLIENT_ID
        scope = settings.OAUTH_SCOPE

        if redirect_uri and len(redirect_uri) > 0:
            try:
                URLValidator(redirect_uri)
                uri_obj = dict(
                    uri="{}?redirect_uri={}&prompt=consent&response_type=code&client_id={}&scope={}"
                        .format(base_uri, redirect_uri, client_id, scope)
                )
                return Response(uri_obj)
            except ValidationError as exception:
                return Response(dict(error="bad redirect_uri"), status=status.HTTP_400_BAD_REQUEST)
        return Response(dict(error="missing redirect_uri"), status=status.HTTP_400_BAD_REQUEST)


class JWTToken(APIView):
    def post(self, request):
        return Response({})
