from django.urls import path
from . import views

urlpatterns = [
    path('shutdown/', views.shutdown),
    path('pause_media/', views.pause_media),
]
