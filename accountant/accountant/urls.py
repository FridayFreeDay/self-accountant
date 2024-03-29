"""
URL configuration for accountant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve as mediaserve

from information.views import page_not_found


urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),

    path('admin/', admin.site.urls),

    path("", include("information.urls")),
    path("users/", include("users.urls", namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
            re_path(f"^{settings.MEDIA_URL.lstrip('/')}(?P<path>.*)$",
            mediaserve, {'document_root': settings.MEDIA_ROOT}),
            re_path(f"^{settings.STATIC_URL.lstrip('/')}(?P<path>.*)$",
            mediaserve, {'document_root': settings.STATIC_ROOT})
        ]

# Отлов ошибок страница не найдена
handler404 = page_not_found