from rest_framework import serializers
from .models import Conversation
from user.models import CustomUser

# custom user serilaizer
class UserSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


# conversation serializer
class ConversationSerializer(serializers.ModelSerializer):
    initiator = UserSerilaizer()
    reciever = UserSerilaizer()
    class Meta:
        model = Conversation
        fields = ['initiator','reciever','start_time']