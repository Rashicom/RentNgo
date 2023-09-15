import json

from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        print("connecting ....")
        user = self.scope["user"]
        print(user)
        self.accept()
        

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message)
        print("returning message back to the user")
        self.send(text_data=json.dumps({"message": message}))
        