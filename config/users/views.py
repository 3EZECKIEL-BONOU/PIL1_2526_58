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
    Un même email peut cumuler les rôles mentor ET mentoré.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email      = request.data.get('email', '').strip()
        is_mentor  = request.data.get('is_mentor', False)
        is_mentee  = request.data.get('is_mentee', False)
        password   = request.data.get('password', '')

        existing = Utilisateur.objects.filter(email=email).first()
        if existing:
            auth_user = authenticate(username=existing.username, password=password)
            if not auth_user:
                return Response(
                    {"error": "Cet email est déjà enregistré. Vérifiez votre mot de passe pour y ajouter un rôle."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            changed, parts = False, []
            if is_mentor and not existing.is_mentor:
                existing.is_mentor = True; changed = True; parts.append("Mentor")
            if is_mentee and not existing.is_mentee:
                existing.is_mentee = True; changed = True; parts.append("Mentoré")
            if not changed:
                return Response(
                    {"error": "Ce compte possède déjà ce(s) rôle(s)."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            existing.save()
            refresh = RefreshToken.for_user(existing)
            return Response({
                "message": f"Rôle(s) {' et '.join(parts)} ajouté(s) à votre compte.",
                "user": ProfilSerializer(existing).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        serializer = InscriptionSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Compte créé avec succès",
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
        email    = (request.data.get('email') or request.data.get('username', '')).strip()
        password = request.data.get('password', '')

        if not email or not password:
            return Response({
                "error": "L'email et le mot de passe sont requis"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_obj = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            return Response({
                "error": "Email ou mot de passe incorrect"
            }, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=user_obj.username, password=password)

        if user is None:
            return Response({
                "error": "Email ou mot de passe incorrect"
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
