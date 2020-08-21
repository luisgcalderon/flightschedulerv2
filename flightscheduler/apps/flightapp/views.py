from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser

from .serializer import UserSerializer, ScheduleSerializer
from .models import Schedule



# Create your views here.
def index(request):
    return HttpResponse("<h1>Hello, Flight Scheduler!</h1>")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# APIS
# /flights/

@csrf_exempt
def flight_list(request):
    # Get all
    if request.method == 'GET':
        schedules = Schedule.objects.all()
        schedules_serializer = ScheduleSerializer(schedules, many=True)
        return JsonResponse(schedules_serializer.data, safe=False)
    # Add
    elif request.method == 'POST':
        schedule_data = JSONParser().parse(request)
        schedules_serializer = ScheduleSerializer(data=schedule_data)
        if schedules_serializer.is_valid():
            schedules_serializer.save()
            return JsonResponse(schedule_data.data, 
                                status=status.HTTP_201_CREATED)
        return JsonResponse(schedules_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Delete all
    elif request.method == 'DELETE':
        Schedule.objects.all().delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    pass

@csrf_exempt
def flight_detail(request, pk):
    try:
        schedule = Schedule.objects.get(pk=pk)
    except Schedule.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # Retrieve one
    if request.method == 'GET':
        schedule_serializer = ScheduleSerializer(schedule)
        return JsonResponse(schedule_serializer.data)

    #Update one record
    if request.method == 'PUT':
        schedule_data = JSONParser().parse(request)
        schedule_serializer = ScheduleSerializer(schedule, data, schedule_data)
        if schedule_serializer.is_valid():
            scheduler_serializer.save()
            return JsonResponse(schedule_serializer.data)
        return JsonResponse(schedule_resializer.error.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        schedule.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        
