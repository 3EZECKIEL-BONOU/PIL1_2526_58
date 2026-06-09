from django.db import models
from django.contrib.auth import get_user_model
Utilisateur = get_user_model()

class Conversation(models.Model):
    createur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="conversations_creees")
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="conversations_recues")
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.createur} -> {self.destinataire}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expediteur} : {self.contenu[:30]}"