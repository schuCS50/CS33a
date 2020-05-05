# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


# Consumer to handle websockets for TicTacToe gameplay
class TicTacToeConsumer(WebsocketConsumer):
    # Connect view for intial connect
    def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = 'game_%s' % self.game_id

        # Join game channel layer
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave game
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        game_data_json = json.loads(text_data)
        location = game_data_json['location']
        user = game_data_json['user']

        # Send to game layer
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': 'game_move',
                'location': location,
                'user': user
            }
        )

    # Function for how to pass info
    def game_move(self, event):
        location = event['location']
        user = event['user']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'location': location,
            'user': user
        }))


# Chat WebSocket Example
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']

        print(self.scope["user"])

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        print(self.channel_name)
        print(self.room_group_name)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
