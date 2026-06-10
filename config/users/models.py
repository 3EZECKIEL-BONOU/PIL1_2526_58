from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('etudiant', 'Etudiant'),
        ('mentor', 'Mentor'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')

    def __str__(self):
        return self.username