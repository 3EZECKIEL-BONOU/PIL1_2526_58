from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

FORMAT_CHOICES = [
    ('présentiel', 'Présentiel'),
    ('en ligne', 'En ligne'),
    ('les deux', 'Les deux'),
]

STATUT_REPONSE_CHOICES = [
    ('en attente', 'En attente'),
    ('accepté', 'Accepté'),
    ('refusé', 'Refusé'),
]

STATUT_SESSION_CHOICES = [
    ('upcoming', 'À venir'),
    ('done', 'Terminée'),
    ('cancelled', 'Annulée'),
]

JOUR_CHOICES = [
    ('Lundi', 'Lundi'),
    ('Mardi', 'Mardi'),
    ('Mercredi', 'Mercredi'),
    ('Jeudi', 'Jeudi'),
    ('Vendredi', 'Vendredi'),
    ('Samedi', 'Samedi'),
    ('Dimanche', 'Dimanche'),
]


class Matiere(models.Model):
    nom_matiere = models.CharField(max_length=150, unique=True)

    class Meta:
        db_table = 'matieres'

    def __str__(self):
        return self.nom_matiere


class CreneauHoraire(models.Model):
    jour = models.CharField(max_length=20, choices=JOUR_CHOICES)
    periode = models.CharField(max_length=50)

    class Meta:
        db_table = 'crenaux_horaires'

    def __str__(self):
        return f"{self.jour} - {self.periode}"


class UtilisateurCompetence(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competences')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        db_table = 'utilisateur_competences'
        unique_together = ('utilisateur', 'matiere')


class UtilisateurLacune(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lacunes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        db_table = 'utilisateur_lacunes'
        unique_together = ('utilisateur', 'matiere')


class UtilisateurDisponibilite(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disponibilites')
    creneau = models.ForeignKey(CreneauHoraire, on_delete=models.CASCADE)

    class Meta:
        db_table = 'utilisateur_disponibilites'
        unique_together = ('utilisateur', 'creneau')


class AnnonceMentorat(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='annonces')
    type_annonce = models.CharField(max_length=20, choices=[('offre','Offre'),('demande','Demande')])
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    format_propose = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    description = models.TextField(blank=True, null=True)
    disponibilite = models.CharField(max_length=200, blank=True, null=True)
    statut = models.CharField(max_length=20, default='active')
    nb_reponses = models.IntegerField(default=0)
    date_publication = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'annonces_mentorat'


class ReponseOffre(models.Model):
    annonce = models.ForeignKey(AnnonceMentorat, on_delete=models.CASCADE, related_name='reponses')
    postulant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reponses_envoyees')
    statut = models.CharField(max_length=20, choices=STATUT_REPONSE_CHOICES, default='en attente')
    message_accompagnement = models.TextField(blank=True, null=True)
    date_reponse = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reponses_offre'


class Session(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions_mentor')
    mentore = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions_mentore')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    date = models.DateField()
    heure = models.TimeField()
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_SESSION_CHOICES, default='upcoming')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sessions'