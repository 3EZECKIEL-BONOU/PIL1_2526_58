from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('me/', ProfileAPIView.as_view()),
    path('change-password/', ChangePasswordAPIView.as_view()),
]