from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.shortcuts import redirect


urlpatterns = [
    path("", lambda r: redirect("/index")),
    path("admin/", admin.site.urls),
    path("", include("myapp.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
