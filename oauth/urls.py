from django.urls import path, include
from .views import ConsentURI, JWTToken

urlpatterns = [
    path('get-consent-page-uri/', ConsentURI.as_view()),
    path('exchange-auth-code-for-jwt/', JWTToken.as_view()),
]
