"""
URLs principales du projet IFRIMentorLink
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

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
    # FUTURS MODULES
    # =====================================================
    path(
        'api/users/', include('users.urls')
    ),
    # path('api/mentorship/', include('mentorship.urls')),
]