"""
============================================================
 IFRI MentorLink — Module Matching
 Fichier : matching/views.py
 Rôle    : Vues API (JSON) pour le matching, les demandes
           et les sessions de mentorat
============================================================
"""

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Utilisateur, AnnonceMentorat, UtilisateurDisponibilite
# Importez vos modèles Session et Demande si vous les avez déjà.
# Sinon, nous vous montrons la structure attendue en commentaire.
# from .models import Session, DemandesMentorat


# ══════════════════════════════════════════════════════════
#  UTILITAIRES INTERNES
# ══════════════════════════════════════════════════════════

def _calculer_score(etudiant, annonce_mentor):
    """
    Calcule un score de compatibilité (0–100) entre un étudiant
    et une annonce de mentorat.
    """
    score = 0
    mentor = annonce_mentor.auteur

    # Même filière
    if etudiant.filiere == mentor.filiere:
        score += 15

    # Niveau d'études (mentor plus avancé = meilleur)
    if "Master" in mentor.niveau_etudes and "Licence" in etudiant.niveau_etudes:
        score += 15
    elif mentor.niveau_etudes == etudiant.niveau_etudes:
        score += 10

    # Créneaux communs (max 40 pts)
    dispos_etudiant = set(
        UtilisateurDisponibilite.objects
        .filter(utilisateur=etudiant)
        .values_list('creneau_id', flat=True)
    )
    dispos_mentor = set(
        UtilisateurDisponibilite.objects
        .filter(utilisateur=mentor)
        .values_list('creneau_id', flat=True)
    )
    creneaux_communs = dispos_etudiant & dispos_mentor
    score += min(len(creneaux_communs) * 10, 40)

    # Lacune de l'étudiant couverte par l'annonce (max 30 pts)
    if etudiant.lacunes.filter(matiere=annonce_mentor.matiere).exists():
        score += 30
    else:
        score += 15

    return score


def _serialiser_mentor(utilisateur):
    """Retourne un dict simplifié d'un utilisateur mentor."""
    return {
        'id'            : utilisateur.id,
        'nom'           : utilisateur.nom,
        'prenom'        : utilisateur.prenom,
        'filiere'       : utilisateur.filiere,
        'niveau_etudes' : utilisateur.niveau_etudes,
        'bio'           : getattr(utilisateur, 'bio', ''),
    }


def _serialiser_matiere(matiere):
    """Retourne un dict simplifié d'une matière."""
    if matiere is None:
        return None
    return {
        'id' : matiere.id,
        'nom': matiere.nom,
    }


# ══════════════════════════════════════════════════════════
#  ENDPOINT : GET /api/matching/
#  Retourne les recommandations de mentors pour l'étudiant
# ══════════════════════════════════════════════════════════

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liste_matching(request):
    """
    Retourne la liste des mentors recommandés pour l'étudiant connecté,
    triée par score décroissant.

    Réponse :
    {
      "recommendations": [
        {
          "mentor": { id, nom, prenom, filiere, niveau_etudes, bio },
          "offre":  { id, matiere: { id, nom }, format },
          "score":  92,
          "horaires_communs": ["Lundi (matin)", "Mercredi (après-midi)"]
        },
        ...
      ]
    }
    """
    # Récupérer le profil étudiant
    try:
        etudiant = request.user.profile
    except ObjectDoesNotExist:
        return Response(
            {'detail': "Votre profil étudiant n'est pas encore complété."},
            status=status.HTTP_400_BAD_REQUEST
        )

    offres = (
        AnnonceMentorat.objects
        .filter(type_annonce='offre')
        .select_related('auteur', 'matiere')
    )

    resultats = []

    for offre in offres:
        # On ne se recommande pas soi-même
        if offre.auteur == etudiant:
            continue

        score = _calculer_score(etudiant, offre)

        # Seuil minimum de pertinence
        if score < 20:
            continue

        # Créneaux communs lisibles
        dispos_etudiant = set(
            UtilisateurDisponibilite.objects
            .filter(utilisateur=etudiant)
            .values_list('creneau__jour', 'creneau__periode')
        )
        dispos_mentor = set(
            UtilisateurDisponibilite.objects
            .filter(utilisateur=offre.auteur)
            .values_list('creneau__jour', 'creneau__periode')
        )
        horaires_communs = [
            f"{jour} ({periode})"
            for jour, periode in dispos_etudiant & dispos_mentor
        ]

        resultats.append({
            'mentor'          : _serialiser_mentor(offre.auteur),
            'offre'           : {
                'id'     : offre.id,
                'matiere': _serialiser_matiere(offre.matiere),
                'format' : getattr(offre, 'format', 'En ligne'),
            },
            'score'           : score,
            'horaires_communs': horaires_communs,
        })

    # Tri par score décroissant
    resultats.sort(key=lambda x: x['score'], reverse=True)

    return Response({'recommendations': resultats})


# ══════════════════════════════════════════════════════════
#  ENDPOINT : GET /api/matching/mes-mentors/
#  Retourne les mentors déjà actifs de l'étudiant
# ══════════════════════════════════════════════════════════

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mes_mentors(request):
    """
    Retourne la liste des mentors avec lesquels l'étudiant
    a déjà une relation active (a envoyé un message ou une demande).

    Réponse :
    {
      "mentors": [ { mentor: {...}, score: int, horaires_communs: [...] }, ... ]
    }

    NOTE : Adaptez la requête selon votre modèle de relation mentor/étudiant.
    """
    try:
        etudiant = request.user.profile
    except ObjectDoesNotExist:
        return Response({'mentors': []})

    # Exemple : récupérer via les messages envoyés
    # À adapter selon votre modèle réel
    # from messaging.models import Message
    # mentor_ids = Message.objects.filter(
    #     expediteur=etudiant
    # ).values_list('destinataire_id', flat=True).distinct()
    # mentors = Utilisateur.objects.filter(id__in=mentor_ids)

    # Placeholder — à remplacer par votre logique
    mentors_data = []

    return Response({'mentors': mentors_data})


# ══════════════════════════════════════════════════════════
#  ENDPOINTS : /api/matching/demandes/
#  GET  → liste des demandes de l'étudiant
#  POST → créer une nouvelle demande
# ══════════════════════════════════════════════════════════

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def demandes(request):
    """
    GET  → liste des demandes de mentorat de l'étudiant connecté.
    POST → créer une nouvelle demande de mentorat.

    Corps POST attendu :
    {
      "matiere": "Python",
      "description": "Je cherche de l'aide pour...",
      "format": "En ligne",
      "disponibilite": "Lundi 14h-17h"
    }
    """
    try:
        etudiant = request.user.profile
    except ObjectDoesNotExist:
        return Response(
            {'detail': 'Profil introuvable.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ── GET ──────────────────────────────────────────────
    if request.method == 'GET':
        # NOTE : Adaptez selon votre modèle DemandesMentorat réel
        # demandes_qs = DemandesMentorat.objects.filter(auteur=etudiant).order_by('-date_creation')
        # data = [_serialiser_demande(d) for d in demandes_qs]
        # return Response({'demandes': data})

        # Placeholder
        return Response({'demandes': []})

    # ── POST ─────────────────────────────────────────────
    matiere      = request.data.get('matiere', '').strip()
    description  = request.data.get('description', '').strip()
    format_cours = request.data.get('format', 'En ligne')
    disponibilite = request.data.get('disponibilite', '')

    if not matiere or not description:
        return Response(
            {'detail': 'Les champs matiere et description sont obligatoires.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # NOTE : Créez l'objet avec votre modèle réel
    # demande = DemandesMentorat.objects.create(
    #     auteur=etudiant,
    #     matiere=matiere,
    #     description=description,
    #     format=format_cours,
    #     disponibilite=disponibilite,
    #     statut='active',
    # )
    # return Response(_serialiser_demande(demande), status=status.HTTP_201_CREATED)

    # Placeholder (à remplacer quand le modèle est prêt)
    now = timezone.now()
    return Response({
        'id'           : None,
        'matiere'      : {'id': None, 'nom': matiere},
        'description'  : description,
        'format'       : format_cours,
        'disponibilite': disponibilite,
        'date_creation': now.isoformat(),
        'statut'       : 'active',
        'nb_reponses'  : 0,
    }, status=status.HTTP_201_CREATED)


# ══════════════════════════════════════════════════════════
#  ENDPOINT : PATCH /api/matching/demandes/<id>/cloturer/
#  Clôture une demande de mentorat
# ══════════════════════════════════════════════════════════

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def cloturer_demande(request, demande_id):
    """
    Clôture une demande de mentorat appartenant à l'étudiant connecté.
    """
    try:
        etudiant = request.user.profile
    except ObjectDoesNotExist:
        return Response({'detail': 'Profil introuvable.'}, status=status.HTTP_400_BAD_REQUEST)

    # NOTE : Adaptez à votre modèle réel
    # try:
    #     demande = DemandesMentorat.objects.get(id=demande_id, auteur=etudiant)
    # except DemandesMentorat.DoesNotExist:
    #     return Response({'detail': 'Demande introuvable.'}, status=status.HTTP_404_NOT_FOUND)
    #
    # demande.statut = 'cloturee'
    # demande.save()
    # return Response(_serialiser_demande(demande))

    return Response({'detail': 'Demande clôturée.'})


# ══════════════════════════════════════════════════════════
#  ENDPOINTS : /api/matching/sessions/
#  GET  → liste des sessions (filtrées par statut)
#  POST → créer une demande de session
# ══════════════════════════════════════════════════════════

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sessions(request):
    """
    GET  ?statut=upcoming → sessions à venir
    GET  ?statut=done     → sessions passées
    POST → créer une demande de session

    Corps POST attendu :
    {
      "mentor_id": 3,
      "matiere": "Python",
      "date": "2025-06-15",
      "heure": "14:00",
      "format": "En ligne"
    }
    """
    try:
        etudiant = request.user.profile
    except ObjectDoesNotExist:
        return Response({'detail': 'Profil introuvable.'}, status=status.HTTP_400_BAD_REQUEST)

    # ── GET ──────────────────────────────────────────────
    if request.method == 'GET':
        statut = request.query_params.get('statut', 'upcoming')
        # NOTE : Adaptez à votre modèle Session réel
        # if statut == 'upcoming':
        #     qs = Session.objects.filter(etudiant=etudiant, date__gte=timezone.now()).order_by('date')
        # else:
        #     qs = Session.objects.filter(etudiant=etudiant, date__lt=timezone.now()).order_by('-date')
        # data = [_serialiser_session(s) for s in qs]
        # return Response({'sessions': data})

        return Response({'sessions': []})

    # ── POST ─────────────────────────────────────────────
    mentor_id = request.data.get('mentor_id')
    matiere   = request.data.get('matiere', '').strip()
    date_str  = request.data.get('date', '')
    heure     = request.data.get('heure', '')
    format_s  = request.data.get('format', 'En ligne')

    if not mentor_id or not date_str:
        return Response(
            {'detail': 'mentor_id et date sont obligatoires.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        mentor = Utilisateur.objects.get(id=mentor_id)
    except Utilisateur.DoesNotExist:
        return Response({'detail': 'Mentor introuvable.'}, status=status.HTTP_404_NOT_FOUND)

    # NOTE : Créez avec votre modèle Session réel
    # session = Session.objects.create(
    #     etudiant=etudiant,
    #     mentor=mentor,
    #     matiere=matiere,
    #     date=date_str,
    #     heure=heure,
    #     format=format_s,
    #     statut='En attente',
    # )
    # return Response(_serialiser_session(session), status=status.HTTP_201_CREATED)

    return Response({
        'id'        : None,
        'matiere'   : {'id': None, 'nom': matiere},
        'mentor_nom': f"{mentor.prenom} {mentor.nom}",
        'date'      : date_str,
        'heure'     : heure,
        'format'    : format_s,
        'statut'    : 'En attente',
    }, status=status.HTTP_201_CREATED)


# ══════════════════════════════════════════════════════════
#  ENDPOINT : PATCH /api/matching/sessions/<id>/annuler/
#  Annule une session
# ══════════════════════════════════════════════════════════

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def annuler_session(request, session_id):
    """Annule une session appartenant à l'étudiant connecté."""
    # NOTE : Adaptez à votre modèle Session réel
    # try:
    #     etudiant = request.user.profile
    #     session = Session.objects.get(id=session_id, etudiant=etudiant)
    # except (ObjectDoesNotExist, Session.DoesNotExist):
    #     return Response({'detail': 'Session introuvable.'}, status=status.HTTP_404_NOT_FOUND)
    #
    # session.statut = 'Annulée'
    # session.save()
    # return Response(_serialiser_session(session))

    return Response({'detail': 'Session annulée.'})
