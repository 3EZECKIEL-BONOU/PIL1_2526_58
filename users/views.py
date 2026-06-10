from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from .serializers import (
    InscriptionSerializer,
    ProfilSerializer,
    ModifierMotDePasseSerializer
)

Utilisateur = get_user_model()


class RegisterAPIView(APIView):
    """
    Vue pour l'inscription des utilisateurs.
    Permet de créer un nouveau compte mentor ou mentoré.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InscriptionSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "Utilisateur créé avec succès",
                "user": ProfilSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    Vue pour l'authentification des utilisateurs.
    Retourne les tokens JWT et les informations de l'utilisateur (incluant ses rôles).
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                "error": "Le nom d'utilisateur et le mot de passe sont requis"
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({
                "error": "Nom d'utilisateur ou mot de passe incorrect"
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Générer les tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": "Connexion réussie",
            "user": ProfilSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "redirect_to": get_redirect_dashboard(user),
        }, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    """
    Vue pour récupérer et modifier le profil de l'utilisateur connecté.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Récupère le profil de l'utilisateur connecté"""
        serializer = ProfilSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """Met à jour le profil de l'utilisateur connecté"""
        serializer = ProfilSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profil mis à jour avec succès",
                "user": serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    """
    Vue pour changer le mot de passe de l'utilisateur connecté.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ModifierMotDePasseSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Mot de passe modifié avec succès"
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_redirect_dashboard(user):
    """
    Détermine vers quel dashboard rediriger l'utilisateur en fonction de ses rôles.
    
    - Si mentor ET mentoré : retourne les deux dashboards disponibles
    - Si seulement mentor : dashboard mentor
    - Si seulement mentoré : dashboard mentoré
    """
    roles = user.get_roles_list()
    
    if len(roles) == 2:  # Mentor ET Mentoré
        return {
            "primary": "dashboardmentor.html",
            "secondary": "dashboardmentee.html",
            "message": "Vous êtes mentor et mentoré. Dashboard mentor par défaut."
        }
    elif user.is_mentor:
        return "dashboardmentor.html"
    elif user.is_mentee:
        return "dashboardmentee.html"
    else:
        return "index.html"
