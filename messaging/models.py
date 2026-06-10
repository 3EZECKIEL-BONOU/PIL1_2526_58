from django.db import models
from django.conf import settings


class Conversation(models.Model):
    createur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations_creees"
    )

    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations_recues"
    )

    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.createur} -> {self.destinataire}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    expediteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expediteur} : {self.contenu[:30]}"