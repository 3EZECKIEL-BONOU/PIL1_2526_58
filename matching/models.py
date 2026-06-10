from django.db import models
from django.conf import settings


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


class Matiere(models.Model):
    nom_matiere = models.CharField(max_length=150, unique=True)

    class Meta:
        db_table = 'matieres'

    def __str__(self):
        return self.nom_matiere


class CreneauHoraire(models.Model):
    JOUR_CHOICES = (
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche'),
    )

    jour = models.CharField(max_length=20, choices=JOUR_CHOICES)
    periode = models.CharField(max_length=50)

    class Meta:
        db_table = 'crenaux_horaires'

    def __str__(self):
        return f"{self.jour} ({self.periode})"


class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    telephone = models.CharField(max_length=150, unique=True)
    mot_de_passe = models.CharField(max_length=255)
    filiere = models.CharField(max_length=50, choices=FILIERE_CHOICES)
    niveau_etudes = models.CharField(max_length=50, choices=NIVEAU_CHOICES)
    photo_profil = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    class Meta:
        db_table = 'utilisateurs'

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class AnnonceMentorat(models.Model):
    TYPE_CHOICES = (
        ('offre', 'Offre'),
        ('demande', 'Demande'),
    )

    FORMAT_CHOICES = (
        ('présentiel', 'Présentiel'),
        ('en ligne', 'En ligne'),
    )

    type_annonce = models.CharField(max_length=20, choices=TYPE_CHOICES)
    format_propose = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    description = models.TextField(blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='annonces')

    class Meta:
        db_table = 'annonces_mentorat'

    def __str__(self):
        return f"{self.type_annonce} - {self.matiere} par {self.auteur}"


class UtilisateurDisponibilite(models.Model):
    utilisateur = models.ForeignKey(
        Utilisateur, on_delete=models.CASCADE, related_name='disponibilites'
    )
    creneau = models.ForeignKey(CreneauHoraire, on_delete=models.CASCADE)

    class Meta:
        db_table = 'utilisateur_disponibilites'
        unique_together = (('utilisateur', 'creneau'),)


class UtilisateurCompetence(models.Model):
    utilisateur = models.ForeignKey(
        Utilisateur, on_delete=models.CASCADE, related_name='competences'
    )
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        db_table = 'utilisateur_competences'
        unique_together = (('utilisateur', 'matiere'),)


class UtilisateurLacune(models.Model):
    utilisateur = models.ForeignKey(
        Utilisateur, on_delete=models.CASCADE, related_name='lacunes'
    )
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        db_table = 'utilisateur_lacunes'
        unique_together = (('utilisateur', 'matiere'),)


class ReponsesOffre(models.Model):
    annonce = models.ForeignKey(
        AnnonceMentorat, on_delete=models.CASCADE, related_name='reponses'
    )
    postulant = models.ForeignKey(
        Utilisateur, on_delete=models.CASCADE, related_name='reponses_envoyees'
    )
    message = models.TextField(blank=True, null=True)
    date_response = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reponses_offre'


class ProgrammeEtudes(models.Model):
    filiere = models.CharField(max_length=50, choices=FILIERE_CHOICES)
    niveau_etudes = models.CharField(max_length=50, choices=NIVEAU_CHOICES)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        db_table = 'programme_etudes'
        unique_together = (('filiere', 'niveau_etudes', 'matiere'),)


class Profil(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profil"
    )

    bio = models.TextField(blank=True)
    filiere = models.CharField(max_length=100, blank=True)
    niveau = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username


class Matching(models.Model):
    etudiant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="match_etudiant"
    )

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="match_mentor"
    )

    score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.etudiant} -> {self.mentor} ({self.score})"
