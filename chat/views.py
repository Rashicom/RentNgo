from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.urls import reverse
from django.shortcuts import redirect
from user.models import CustomUser
from .models import Conversation
from .serializers import ConversationSerializer
from django.db.models import Q

class StartConversation(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def post(self, request, format=None):
        """
        accept: reciever (to which user we start communication)
        
        this method is start a conversation by start with a lookup in database
        
        collecting all conversations where the the request.user and reciever are participated(only one exist if there is any previous chat)
        if conversation exist collect chat history and return
        if conversation does not exist start a new conversation
        """

        # fetching the reciever
        reciever = request.data.get('reciever')

        # fetching reciever instance for database if exist, else return does not exist message
        try:
            participant = CustomUser.objects.get(email=reciever)
            
        except CustomUser.DoesNotExist:
            return Response({"details":"reciever does not exist"})
        
        # collecting conversation if any
        q_fiter = Q(initiator=request.user.id, reciever=participant.id) | Q(initiator=participant.id, reciever=request.user.id)
        conversation = Conversation.objects.filter(q_fiter)
        
        # if any conversation already exist, fetch the history and return
        if conversation.exists():
            print("conversation found")
            serializer = self.serializer_class(conversation[0])
            
        
        # if no conversation exists, create new conversation
        else:
            conversation = Conversation.objects.create(initiator=request.user, reciever=participant)
            
            # serialize
            serializer = self.serializer_class(conversation)
        
        return Response(serializer.data, status=201)

    


class GetConversations(APIView):

    authentication_classes = []
    permission_classes = []
    serializer_class = ConversationSerializer

    def get(self, request, format=None):
        """
        accept kwargs: conversation_id

        it returns the conversation matched with the given conversation_id
        """

        # fetching conversation_id and user
        conversation_id = request.query_params.get('conversation_id')
        user = request.user

        # fetching conversation from database
        conversation = Conversation.objects.filter(conversation_id=conversation_id)
        
        # if conversation exist serialize and return
        if conversation.exists():
            serializer = self.serializer_class(conversation[0])
            return Response(serializer.data, status=200)
            
        # if no conversation found in that conversation id
        else:
            return Response({"details":"conversation does not found, pleace check the conversation_id"})



class UserConversation(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get(self, request, format=None):
        """
        this method is returnins all conversations  of the requested user
        """

        # fetching user instance
        user = request.user

        # filter all conversation where user weather initiator or a reciever
        q_filter = Q(initiator=user) | Q(reciever=user)
        conversation = Conversation.objects.filter(q_filter)

        # if conversation exist serialize and return response
        if conversation.exists():
            serializer = self.serializer_class(conversation, many=True)
            return Response(serializer.data, status=200)
        
        else:
            return Response({"details":"no conversation found"})




