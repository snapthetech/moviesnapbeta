"""
URL configuration for techsnap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="Techsnap API",
      default_version='v1',
      description="Techsnap",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="adhishraya@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(AllowAny,),
)


handler404 = 'techsnap.views.custom_404'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('auth_modules.urls'),name = "Auth Module"),
    path('posts/',include('notifications.urls'),name='post'),
    path('movies/',include('movies.urls'),name = 'movies'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
