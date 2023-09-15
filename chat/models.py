from django.db import models
from user.models import CustomUser
import uuid

# Create your models here.
# one to one communication database


class Conversation(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    room = models.UUIDField(default=uuid.uuid4, unique=True)
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
        ordering = ('-timestamp',)

