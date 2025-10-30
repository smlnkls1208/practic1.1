from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('', include('main.urls')),
]