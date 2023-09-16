from rest_framework import serializers
from .models import Conversation, Messages
from user.models import CustomUser

# custom user serilaizer
class UserSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','contact_number','profile_photo']


# message
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['sender','text','timestamp']


# conversation serializer
class ConversationSerializer(serializers.ModelSerializer):
    initiator = UserSerilaizer()
    reciever = UserSerilaizer()
    class Meta:
        model = Conversation
        fields = ['room','initiator','reciever','start_time']
    

# conversaton message history
class ConversationMessageSerializer(serializers.ModelSerializer):
    message_set = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['room','message_set']
        