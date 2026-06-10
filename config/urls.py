"""
URLs principales du projet IFRIMentorLink
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from config.users.views import LoginAPIView

urlpatterns = [

    # =====================================================
    # ROOT-LEVEL STATIC FILES (CSS, JS served at root path)
    # =====================================================
    re_path(r'^(?P<path>(style|connexion|etuinscri|rapport)\.css)$', serve, {'document_root': settings.BASE_DIR}),
    re_path(r'^(?P<path>(script|api)\.js)$', serve, {'document_root': settings.BASE_DIR}),

    # =====================================================
    # FRONTEND HTML PAGES
    # =====================================================
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('connexion/', TemplateView.as_view(template_name='connexion.html'), name='connexion'),
    path('inscription/', TemplateView.as_view(template_name='etuinscri.html'), name='inscription'),
    path('dashboard/mentor/', TemplateView.as_view(template_name='dashboardmentor.html'), name='dashboard_mentor'),
    path('dashboard/mentee/', TemplateView.as_view(template_name='dashboardmentee.html'), name='dashboard_mentee'),
    path('rapport/', TemplateView.as_view(template_name='rapport.html'), name='rapport'),


    # =====================================================
    # ADMIN DJANGO
    # =====================================================
    path('admin/', admin.site.urls),

    # =====================================================
    # AUTHENTIFICATION JWT
    # =====================================================
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # =====================================================
    # MODULES API
    # =====================================================
    path(
        'api/messaging/',
        include('messaging.urls')
    ),

    path(
        'api/notifications/',
        include('notifications.urls')
    ),

    path(
        'api/matching/',
        include('matching.urls')
    ),

    # =====================================================
    # USERS API
    # =====================================================
    path(
        'api/users/',
        include('config.users.urls')
    ),

    # =====================================================
    # LOGIN SHORTCUT
    # =====================================================
    path(
        'api/login/',
        LoginAPIView.as_view(),
        name='login'
    ),
]