from django.db.models.signals import post_save
from django.dispatch import receiver
from messaging.models import Message
from .models import Notification


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        conversation = instance.conversation

        # trouver le destinataire (pas le sender)
        recipients = conversation.participants.exclude(id=instance.sender.id)

        for user in recipients:
            Notification.objects.create(
                utilisateur=user,
                type_notif="message",
                contenu=f"Nouveau message de {instance.sender}",
                lu=False
            )