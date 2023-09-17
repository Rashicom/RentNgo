import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        """
        this method establishing long lived connection with the user
        accept : room_name (format:UUID)
                 tocken (in params named as tocken, jwt)
        
        WARNING: this method is called only if the tocken is validated, routing is wraped by jwt authentication class in the asgi config

        """

        print("connecting ....")

        # fetchind authenticated user instance and room_name
        user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
        self.room_group_name = f"chat_{self.room_name}"

        print(user)
        """
        By default the send(), group_send(), group_add() and other functions are async functions, 
        meaning you have to await them. If you need to call them from synchronous code, 
        you'll need to use the handy asgiref.sync.async_to_sync wrapper:
        """
        # join room group
        # here async_to_sync(self.channel_layer.group_add) returning another function
        # converting group_add async function to sync function
        sync_group_add = async_to_sync(self.channel_layer.group_add)
        
        # channel_name is defined by django when a websocket connection created
        # every socket connection have a unique channel_name it represent wich user is conneted from a instace
        # now we are including this websicket connection to send/recive message from room_group_name
        sync_group_add(self.room_group_name,self.channel_name)
        
        

        self.accept()
        

    def disconnect(self, close_code):
        pass
    

    # Receive message from WebSocket
    def receive(self, text_data):

        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        # send the message to the group which socket connected to
        # a function named as chat_message must be defined to handle / recieve message
        # type is usefull to call defferent fuction based on the recieve state like typing.., chat_message
        chat_type = {"type": "chat_message"}
        return_dict = {**chat_type, **text_data_json}

        # get a sync function for sending message
        sync_send = async_to_sync(self.channel_layer.group_send)
        
        # send message to the room which we connected to
        sync_send(self.room_group_name, return_dict)


    # Receive message from room group
    def chat_message(self, event):
        """
        this fuction is called if the chat_type is chat_message
        means message is sended
        """

        # copy the event, becouse this is a async and longlived connection 
        # another user and functin may use the same data, so we have to proserve
        # by coping we assert that original message wont interepted
        text_data_json = event.copy()

        print(text_data_json)
        
        # getting message and attachments. attachments is may or may not be present in the data. thats why we use .get()
        message, attachments = (text_data_json["message"], text_data_json.get("attachments"))

        # sava the data in to the database
        print("////////////////")
        print("sender:",self.scope["user"])
        print(message)
        print(attachments)
        print("////////////////")

        # then send to message to the websocket target user can see the message
        self.send(text_data=json.dumps(text_data_json))

        