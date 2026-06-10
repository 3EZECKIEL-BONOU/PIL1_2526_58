from django.contrib import admin
from .models import (
    Utilisateur, AnnonceMentorat, CreneauHoraire,
    UtilisateurDisponibilite, Matiere, UtilisateurLacune,
    UtilisateurCompetence, ReponsesOffre, ProgrammeEtudes,
    Profil, Matching
)

admin.site.register(Utilisateur)
admin.site.register(AnnonceMentorat)
admin.site.register(CreneauHoraire)
admin.site.register(UtilisateurDisponibilite)
admin.site.register(Matiere)
admin.site.register(UtilisateurLacune)
admin.site.register(UtilisateurCompetence)
admin.site.register(ReponsesOffre)
admin.site.register(ProgrammeEtudes)
admin.site.register(Profil)
admin.site.register(Matching)
