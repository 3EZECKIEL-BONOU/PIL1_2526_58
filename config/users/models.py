from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('etudiant', 'Etudiant'),
        ('mentor', 'Mentor'),
        ('admin', 'Admin'),
    )

    FILIERE_CHOICES = (
        ('Génie Logiciel', 'Génie Logiciel'),
        ('Intelligence Artificielle', 'Intelligence Artificielle'),
        ('Internet et multimédia', 'Internet et multimédia'),
        ('Sécurité Informatique', 'Sécurité Informatique'),
    )

    NIVEAU_CHOICES = (
        ('License 1', 'License 1'),
        ('License 2', 'License 2'),
        ('License 3', 'License 3'),
        ('Master 1', 'Master 1'),
        ('Master 2', 'Master 2'),
        ('Master 3', 'Master 3'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')

    nom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    is_mentor = models.BooleanField(default=False)
    is_mentee = models.BooleanField(default=True)
    filiere = models.CharField(max_length=50, choices=FILIERE_CHOICES, blank=True)
    niveau_etudes = models.CharField(max_length=50, choices=NIVEAU_CHOICES, blank=True)
    bio = models.TextField(blank=True)
    photo_profil = models.CharField(max_length=255, blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def get_roles_list(self):
        roles = []
        if self.is_mentor:
            roles.append('mentor')
        if self.is_mentee:
            roles.append('mentee')
        return roles

    def __str__(self):
        return self.username