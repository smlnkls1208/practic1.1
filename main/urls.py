from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('create-request/', views.create_request, name='create_request'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('delete-request/<int:request_id>/', views.delete_request, name='delete_request'),

]