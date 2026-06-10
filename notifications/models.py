from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = (
        ('message', 'Message'),
        ('system', 'System'),
    )

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    type_notif = models.CharField(max_length=50, choices=TYPE_CHOICES)
    contenu = models.TextField()
    lu = models.BooleanField(default=False)
    date_notification = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur} - {self.contenu[:30]}"