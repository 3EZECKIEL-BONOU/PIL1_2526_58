from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('etudiant', 'Étudiant'),
        ('mentor', 'Mentor'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    telephone = models.CharField(max_length=20, blank=True, null=True)

    filiere = models.CharField(max_length=100, blank=True, null=True)

    niveau_etudes = models.CharField(max_length=100, blank=True, null=True)

    bio = models.TextField(blank=True, null=True)

    photo_profil = models.ImageField(upload_to='profiles/', blank=True, null=True)

    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"