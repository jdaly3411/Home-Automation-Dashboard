from django.urls import path
from .views import SensorDataView, ControlDeviceView

urlpatterns = [
    path('sensor-data/', SensorDataView.as_view(), name='sensor-data'),
    path('control-device/', ControlDeviceView.as_view(), name='control-device'),
]
