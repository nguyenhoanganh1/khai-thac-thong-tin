from django.urls import path
from . import views

urlpatterns = [
    path('/manual', views.manual),
    path('/lib', views.lib),
]