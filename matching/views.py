from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Utilisateur, AnnonceMentorat, UtilisateurDisponibilite

def calculer_score_matching(etudiant, annonce_mentor):
    score = 0
    mentor = annonce_mentor.auteur

    if etudiant.filiere == mentor.filiere:
        score += 15
    
    if "Master" in mentor.niveau_etudes and "License" in etudiant.niveau_etudes:
        score += 15
    elif mentor.niveau_etudes == etudiant.niveau_etudes:
        score += 10

    dispos_etudiant = set(UtilisateurDisponibilite.objects.filter(utilisateur=etudiant).values_list('creneau_id', flat=True))
    dispos_mentor = set(UtilisateurDisponibilite.objects.filter(utilisateur=mentor).values_list('creneau_id', flat=True))
    
    creneaux_communs = dispos_etudiant.intersection(dispos_mentor)
    score += min(len(creneaux_communs) * 10, 40)

    if etudiant.lacunes.filter(matiere=annonce_mentor.matiere).exists():
        score += 30
    else:
        score += 15

    return score


@login_required
def liste_matching(request):
    try:
        etudiant_profil = request.user.profile
    except ObjectDoesNotExist:
        return render(request, 'matching/liste_matching.html', {
            'erreur': "Votre profil étudiant n'est pas encore complété."
        })

    offres_mentors = AnnonceMentorat.objects.filter(type_annonce='offre').select_related('auteur', 'matiere')
    resultats_matching = []

    for offre in offres_mentors:
        if offre.auteur == etudiant_profil:
            continue
            
        score = calculer_score_matching(etudiant_profil, offre)
        
        if score >= 20:
            dispos_etudiant = set(UtilisateurDisponibilite.objects.filter(utilisateur=etudiant_profil).values_list('creneau__jour', 'creneau__periode'))
            dispos_mentor = set(UtilisateurDisponibilite.objects.filter(utilisateur=offre.auteur).values_list('creneau__jour', 'creneau__periode'))
            
            horaires_communs = [f"{j} ({p})" for j, p in dispos_etudiant.intersection(dispos_mentor)]

            resultats_matching.append({
                'offre': offre,
                'mentor': offre.auteur,
                'score': score,
                'horaires_communs': horaires_communs
            })

    resultats_matching = sorted(resultats_matching, key=lambda x: x['score'], reverse=True)

    return render(request, 'matching/liste_matching.html', {'recommendations': resultats_matching})


# Create your views here.
