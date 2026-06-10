from django.db.models.signals import post_save
from django.dispatch import receiver
from messaging.models import Message
from .models import Notification


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        conversation = instance.conversation
        expediteur = instance.expediteur

        # Notify the other participant in the conversation
        destinataire = None
        if conversation.createur == expediteur:
            destinataire = conversation.destinataire
        elif conversation.destinataire == expediteur:
            destinataire = conversation.createur

        if destinataire:
            Notification.objects.create(
                utilisateur=destinataire,
                type_notif='message',
                contenu=f"Nouveau message de {expediteur}",
            )