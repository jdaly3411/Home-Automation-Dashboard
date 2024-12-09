from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SensorData
from .serializer import SensorDataSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

class SensorDataView(APIView):
    permission_classes = [AllowAny]  # Allow all requests for testing
    
    def post(self, request):
        """
        Create a new sensor data entry
        """
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Retrieve the last 10 sensor data entries, ordered by most recent
        """
        # Fetch last 10 entries, sorted by timestamp in descending order
        data = SensorData.objects.all().order_by('-timestamp')[:10]
        serializer = SensorDataSerializer(data, many=True)
        return Response(serializer.data)

class ControlDeviceView(APIView):
    permission_classes = [AllowAny]  # Allow all requests for testing
    
    def post(self, request):
        """
        Send a control command to the Arduino
        """
        command = request.data.get("command")
        if command:
            from .serial_reader import send_to_serial
            try:
                send_to_serial(command)
                return Response({"message": "Command sent successfully!"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "No command provided"}, status=status.HTTP_400_BAD_REQUEST)