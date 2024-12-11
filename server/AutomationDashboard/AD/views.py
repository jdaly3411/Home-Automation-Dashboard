from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SensorData
from .serializer import SensorDataSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from datetime import datetime, time

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
        Retrieve sensor data entries with optional filtering by date and time
        Defaults to last 10 entries if no filters are applied
        """
        # Get filter parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        # Start with all sensor data, sorted by timestamp
        queryset = SensorData.objects.all().order_by('-timestamp')

        # Apply date filters if provided
        if start_date:
            queryset = queryset.filter(timestamp__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__date__lte=end_date)

        # Apply time filters if provided
        if start_time:
            start_datetime = datetime.strptime(start_time, '%H:%M').time()
            queryset = queryset.filter(timestamp__time__gte=start_datetime)
        if end_time:
            end_datetime = datetime.strptime(end_time, '%H:%M').time()
            queryset = queryset.filter(timestamp__time__lte=end_datetime)

        # If no filters are applied, limit to last 10 entries
        if not (start_date or end_date or start_time or end_time):
            queryset = queryset[:10]

        # Serialize and return the data
        serializer = SensorDataSerializer(queryset, many=True)
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