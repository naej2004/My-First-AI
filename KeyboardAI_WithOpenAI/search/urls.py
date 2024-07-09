from django.urls import path
from . import views

app_name = "search"

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('get_response/', views.get_response, name='get_response'),
    path('get_suggestions/', views.get_suggestions, name='get_suggestions'),
]
