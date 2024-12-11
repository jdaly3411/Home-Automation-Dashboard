from django.urls import path
from .views import SensorDataView, ControlDeviceView
from controller import views as controller_views  # Import controller views directly

from . import views

urlpatterns = [
    path('sensor-data/', SensorDataView.as_view(), name='sensor-data'),
    path('control-device/', ControlDeviceView.as_view(), name='control-device'),
    path('shutdown/', controller_views.shutdown, name='shutdown'),
    path('pause-media/', controller_views.pause_media, name='pause-media'),
]
