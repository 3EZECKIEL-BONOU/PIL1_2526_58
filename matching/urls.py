from django.urls import path
from . import views

urlpatterns = [
    path('recommandations/', views.liste_matching, name='liste_matching'),
]