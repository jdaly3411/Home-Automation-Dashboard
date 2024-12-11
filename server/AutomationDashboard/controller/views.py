from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import os
import win32api
import win32con
import time

# Create your views here.
MAC_ADDRESS = "A0-36-BC-2C-4E-54"

@csrf_exempt
def shutdown(request):
    os.system("shutdown /s /t 1") # Shutdown command to shutdown the computer
    return JsonResponse({'message': 'PC is shutting down'})

@csrf_exempt
@require_http_methods(["POST"])
def pause_media(request):
    try:
        VK_MEDIA_PLAY_PAUSE = 0xB3
        win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0, 0)
        time.sleep(0.1)
        win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, win32con.KEYEVENTF_KEYUP, 0)
        
        response = JsonResponse({'message': "Media Paused"})
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        response = JsonResponse({'error': str(e)}, status=500)
        response['Access-Control-Allow-Origin'] = '*'
        return response
