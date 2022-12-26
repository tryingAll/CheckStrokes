from django.urls import path,include
from . import views
urlpatterns = [
path('', views.up, name=''),
path('result', views.result, name='result'),
]
