from django.db.models.signals import post_save
from django.dispatch import receiver
from messaging.models import Message
from .models import Notification


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        conversation = instance.conversation
        expediteur = instance.expediteur

        # Le destinataire est celui qui n'a pas envoyé le message
        if instance.expediteur == conversation.createur:
            destinataire = conversation.destinataire
        else:
            destinataire = conversation.createur

        Notification.objects.create(
            utilisateur=destinataire,
            type_notif="message",
            contenu=f"Nouveau message de {instance.expediteur}",
            lu=False
        )
