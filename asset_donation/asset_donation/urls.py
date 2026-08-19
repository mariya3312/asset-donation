"""
URL configuration for asset_donation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularSwaggerView


@extend_schema_view(get=extend_schema(exclude=True))
class HiddenSpectacularJSONAPIView(SpectacularJSONAPIView):
    pass


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.svg', permanent=True)),
    path('admin/', admin.site.urls),
    path('admin-panel/', include('myapp.admin_panel_urls')),
    path('api/schema/', HiddenSpectacularJSONAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include('myapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

