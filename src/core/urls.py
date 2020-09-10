from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings

from api.urls import urlpatterns


class AddPrefixOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        schema.basePath = '/api'
        return schema

    
schema_view = get_schema_view(
    openapi.Info(
        title="{{ files.0 }} API",
        default_version='v0',
        description="Description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=urlpatterns,
    generator_class=AddPrefixOpenAPISchemaGenerator,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('accounts/', include('allauth.urls')),

    path('api/', include(('api.urls', 'api'), namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
