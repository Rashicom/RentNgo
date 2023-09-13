from django.db import models
from user.models import CustomUser

# Create your models here.

class Conversation(models.Model):
    initiator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='convo_starter')
    reciever = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='convo_participant')
    start_time = models.DateTimeField(auto_now_add=True)


class Messages(models.Model):
    
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='message_sender', null=True)
    text = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # order the message based on the time they send
    class Meta:
        ordering = ('-timestamp')

