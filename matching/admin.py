from django.contrib import admin
from .models import Utilisateur, AnnonceMentorat, CreneauHoraire, UtilisateurDisponibilite, Matiere, UtilisateurLacune

admin.site.register(Utilisateur)
admin.site.register(AnnonceMentorat)
admin.site.register(CreneauHoraire)
admin.site.register(UtilisateurDisponibilite)
admin.site.register(Matiere)
admin.site.register(UtilisateurLacune)


# Register your models here.
