from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import AnnonceMentorat, UtilisateurDisponibilite, UtilisateurLacune

User = get_user_model()


def calculer_score(etudiant, offre):
    score = 0
    mentor = offre.auteur

    # Compatibilité filière
    if etudiant.filiere == mentor.filiere:
        score += 15

    # Compatibilité niveau
    if "Master" in mentor.niveau_etudes and "Licence" in etudiant.niveau_etudes:
        score += 15
    elif mentor.niveau_etudes == etudiant.niveau_etudes:
        score += 10

    # Compatibilité horaires
    dispos_etudiant = set(
        UtilisateurDisponibilite.objects.filter(utilisateur=etudiant)
        .values_list('creneau_id', flat=True)
    )
    dispos_mentor = set(
        UtilisateurDisponibilite.objects.filter(utilisateur=mentor)
        .values_list('creneau_id', flat=True)
    )
    creneaux_communs = dispos_etudiant.intersection(dispos_mentor)
    score += min(len(creneaux_communs) * 10, 40)

    # Compatibilité matière / lacunes
    if UtilisateurLacune.objects.filter(utilisateur=etudiant, matiere=offre.matiere).exists():
        score += 30
    else:
        score += 15

    return score


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liste_matching(request):
    etudiant = request.user

    offres = AnnonceMentorat.objects.filter(
        type_annonce='offre'
    ).select_related('auteur', 'matiere')

    resultats = []

    for offre in offres:
        if offre.auteur == etudiant:
            continue

        score = calculer_score(etudiant, offre)

        if score >= 20:
            dispos_e = set(
                UtilisateurDisponibilite.objects.filter(utilisateur=etudiant)
                .values_list('creneau__jour', 'creneau__periode')
            )
            dispos_m = set(
                UtilisateurDisponibilite.objects.filter(utilisateur=offre.auteur)
                .values_list('creneau__jour', 'creneau__periode')
            )
            horaires_communs = [f"{j} ({p})" for j, p in dispos_e.intersection(dispos_m)]

            resultats.append({
                'mentor': {
                    'id': offre.auteur.id,
                    'nom': offre.auteur.nom,
                    'prenom': offre.auteur.prenom,
                    'filiere': offre.auteur.filiere,
                    'niveau_etudes': offre.auteur.niveau_etudes,
                },
                'offre': {
                    'id': offre.id,
                    'matiere': {
                        'id': offre.matiere.id,
                        'nom': offre.matiere.nom_matiere,
                    },
                    'format': offre.format_propose,
                },
                'score': score,
                'horaires_communs': horaires_communs,
            })

    resultats.sort(key=lambda x: x['score'], reverse=True)

    return Response({'recommendations': resultats})
