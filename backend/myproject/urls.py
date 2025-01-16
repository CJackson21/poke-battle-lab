from django.contrib import admin
from django.urls import path, include
from databases.views import root_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("databases.urls")),
    path("", root_view),
]
