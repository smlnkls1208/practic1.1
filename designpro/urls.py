from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]