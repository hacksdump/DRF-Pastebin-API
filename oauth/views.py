import requests
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.core.validators import URLValidator
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class ConsentURI(APIView):
    def post(self, request):
        base_uri = settings.OAUTH_CONSENT_URI
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
        request_data = request.data
        oauth_token_uri = settings.OAUTH_TOKEN_URI
        redirect_uri = request_data.get('redirect_uri')
        oauth_code = request_data.get('oauth_code')
        client_id = settings.OAUTH_CLIENT_ID
        client_secret = settings.OAUTH_CLIENT_SECRET
        grant_type = "authorization_code"
        errors = dict()
        post_data = dict(
            code=oauth_code,
            redirect_uri=redirect_uri,
            client_id=client_id,
            client_secret=client_secret,
            grant_type=grant_type
        )
        r = requests.post(oauth_token_uri, data=post_data)
        response = r.json()
        if 'error' in response:
            return Response(dict(error='missing_values'), status=status.HTTP_400_BAD_REQUEST)
        access_token = response.get('access_token')
        r = requests.get(settings.OAUTH_EMAIL_URI, params=dict(access_token=access_token))
        oauth_user = r.json()
        email = oauth_user.get('email')

        # create user if not exist
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User()
            user.username = email
            user.email = email
            user.save()

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = dict(
            username=user.username,
            access_token=str(token.access_token),
            refresh_token=str(token),
        )
        return Response(response)
