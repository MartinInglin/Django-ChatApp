from datetime import date
from django.conf import settings
from django.db import models


class Chat(models.Model):
    created_at = models.DateField(default=date.today)


class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateField(default=date.today)
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="chat_message_set",
        default=None,
        blank=True,  # Erlaubnis erteilt, nichts in das Feld zu schreiben
        null=True,  # Ist für die Datenbank, damit akzeptiert sie Null
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # Löscht die Nachricht, wenn der User gelöscht wird
        related_name="author_message_set",  # Braucht es, sonst gibt es einen Fehler. Wird für die Datenbank benötigt
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # Löscht die Nachricht, wenn der User gelöscht wird
        related_name="receiver",  # Braucht es, sonst gibt es einen Fehler. Wird für die Datenbank benötigt
    )
