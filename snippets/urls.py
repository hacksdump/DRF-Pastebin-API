from django.urls import path, include
from snippets.views import SnippetViewSet, UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view

schema_view = get_schema_view(title='Pastebin API')
swagger_view = get_swagger_view(title='Pastebin API')

router = DefaultRouter()
router.register(r'snippets', SnippetViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('schema', schema_view),
    path('swagger', swagger_view),
]
