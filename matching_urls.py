"""
============================================================
 IFRI MentorLink — Module Matching
 Fichier : matching/urls.py
 Rôle    : Routes API du module matching
           (recommandations, demandes, sessions)
============================================================
"""

from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [

    # =====================================================
    # RECOMMANDATIONS DE MENTORS
    # GET /api/matching/
    # → liste des mentors recommandés pour l'étudiant connecté
    # =====================================================
    path(
        '',
        views.liste_matching,
        name='liste_matching'
    ),

    # =====================================================
    # MES MENTORS ACTIFS
    # GET /api/matching/mes-mentors/
    # → mentors avec lesquels l'étudiant a déjà une relation
    # =====================================================
    path(
        'mes-mentors/',
        views.mes_mentors,
        name='mes_mentors'
    ),

    # =====================================================
    # DEMANDES DE MENTORAT
    # GET  /api/matching/demandes/  → liste des demandes
    # POST /api/matching/demandes/  → créer une demande
    # =====================================================
    path(
        'demandes/',
        views.demandes,
        name='demandes'
    ),

    # =====================================================
    # CLÔTURER UNE DEMANDE
    # PATCH /api/matching/demandes/<id>/cloturer/
    # =====================================================
    path(
        'demandes/<int:demande_id>/cloturer/',
        views.cloturer_demande,
        name='cloturer_demande'
    ),

    # =====================================================
    # SESSIONS DE MENTORAT
    # GET  /api/matching/sessions/?statut=upcoming|done
    # POST /api/matching/sessions/  → créer une demande de session
    # =====================================================
    path(
        'sessions/',
        views.sessions,
        name='sessions'
    ),

    # =====================================================
    # ANNULER UNE SESSION
    # PATCH /api/matching/sessions/<id>/annuler/
    # =====================================================
    path(
        'sessions/<int:session_id>/annuler/',
        views.annuler_session,
        name='annuler_session'
    ),
]
