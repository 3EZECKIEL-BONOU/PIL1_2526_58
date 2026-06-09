from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by("-date_notification")
    serializer_class = NotificationSerializer