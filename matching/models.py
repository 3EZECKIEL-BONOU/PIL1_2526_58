from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. TRADUCTION DES ENUMS (LISTES DE CHOIX)
# ==========================================

FILIERE_CHOICES = [
    ('Génie Logiciel', 'Génie Logiciel'),
    ('Intelligence Artificielle', 'Intelligence Artificielle'),
    ('Internet et multimédia', 'Internet et multimédia'),
]

NIVEAU_CHOICES = [
    ('License 1', 'License 1'),
    ('License 2', 'License 2'),
    ('License 3', 'License 3'),
    ('Master 1', 'Master 1'),
    ('Master 2', 'Master 2'),
    ('Master 3', 'Master 3'),
]

FORMAT_COURS_CHOICES = [
    ('présentiel', 'Présentiel'),
    ('en ligne', 'En ligne'),
]

CHOIX_ANNONCE_CHOICES = [
    ('offre', 'Offre'),
    ('demande', 'Demande'),
]

STATUT_REPONSE_CHOICES = [
    ('en attente', 'En attente'),
    ('accepté', 'Accepté'),
    ('refusé', 'Refusé'),
]

TYPE_NOTIFICATION_CHOICES = [
    ('message', 'Message'),
    ('matching', 'Matching'),
    ('système', 'Système'),
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


# ==========================================
# 2. TRADUCTION DES TABLES PRINCIPALES
# ==========================================

class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    telephone = models.CharField(max_length=150, unique=True)
    mot_de_passe = models.CharField(max_length=255) # Stockera le mot de passe
    filiere = models.CharField(max_length=50, choices=FILIERE_CHOICES)
    niveau_etudes = models.CharField(max_length=50, choices=NIVEAU_CHOICES)
    photo_profil = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'utilisateurs' 

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Matiere(models.Model):
    """ Table 'matieres' """
    nom_matiere = models.CharField(max_length=150, unique=True)

    class Meta:
        db_table = 'matieres'

    def __str__(self):
        return self.nom_matiere


class CreneauHoraire(models.Model):
    """ Table 'crenaux_horaires' """
    jour = models.CharField(max_length=20, choices=JOUR_CHOICES)
    periode = models.CharField(max_length=50)

    class Meta:
        db_table = 'crenaux_horaires'

    def __str__(self):
        return f"{self.jour} - {self.periode}"


class ProgrammeEtudes(models.Model):
    """ Table 'programme_etudes' """
    filiere = models.CharField(max_length=50, choices=FILIERE_CHOICES)
    niveau_etudes = models.CharField(max_length=50, choices=NIVEAU_CHOICES)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        db_table = 'programme_etudes'
        unique_together = ('filiere', 'niveau_etudes', 'matiere')


# ==========================================
# 3. TABLES DE LIAISON (COMPÉTENCES, LACUNES, DISPOS)
# ==========================================

class UtilisateurCompetence(models.Model):
    """ Table 'utilisateur_competences' """
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='competences')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        db_table = 'utilisateur_competences'
        unique_together = ('utilisateur', 'matiere')


class UtilisateurLacune(models.Model):
    """ Table 'utilisateur_lacunes' """
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='lacunes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    class Meta:
        db_table = 'utilisateur_lacunes'
        unique_together = ('utilisateur', 'matiere')


class UtilisateurDisponibilite(models.Model):
    """ Table 'utilisateur_disponibilites' """
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='disponibilites')
    creneau = models.ForeignKey(CreneauHoraire, on_delete=models.CASCADE)

    class Meta:
        db_table = 'utilisateur_disponibilites'
        unique_together = ('utilisateur', 'creneau')


# ==========================================
# 4. TRANSACTIONS MENTORAT (MATCHING)
# ==========================================

class AnnonceMentorat(models.Model):
    """ Table 'annonces_mentorat' """
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='annonces')
    type_annonce = models.CharField(max_length=20, choices=CHOIX_ANNONCE_CHOICES)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    format_propose = models.CharField(max_length=20, choices=FORMAT_COURS_CHOICES)
    description = models.TextField(blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'annonces_mentorat'


class ReponseOffre(models.Model):
    """ Table 'reponses_offre' """
    annonce = models.ForeignKey(AnnonceMentorat, on_delete=models.CASCADE, related_name='reponses')
    postulant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='reponses_envoyees')
    statut = models.CharField(max_length=20, choices=STATUT_REPONSE_CHOICES, default='en attente')
    message_accompagnement = models.TextField(blank=True, null=True)
    date_response = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reponses_offre'


# ==========================================
# 5. MESSAGERIE ET NOTIFICATIONS
# ==========================================

class Conversation(models.Model):
    """ Table 'conversations' """
    createur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='conversations_creees')
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='conversations_recues')
    date_envoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversations'


class Message(models.Model):
    """ Table 'messages' """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_envoyes')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'


class Notification(models.Model):
    """ Table 'notifications' """
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    type_notif = models.CharField(max_length=20, choices=TYPE_NOTIFICATION_CHOICES)
    contenu = models.TextField()
    lu = models.BooleanField(default=False)
    date_notification = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'

# Create your models here.
