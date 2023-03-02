import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from room.models import Message, Room
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        room_name = data['room']
        messages = Message.objects.filter(room__room_name=room_name)
        context = {
            "messages": self.messages_to_json(messages),
            "method": "fetch_messages"
        }
        self.load_messages_to_group(context)
        # self.fetch_messages_now(context)

    def new_message(self, data):
        user = data['sender']
        room_name = data['room']
        message_user = User.objects.filter(username=user).first()
        chat_room = Room.objects.filter(room_name=room_name).first()
        message = Message.objects.create(user=message_user, body=data['message'], room=chat_room)
        content = {
            "method": "new_message",
            "message": self.message_to_json(message)
        }
        self.send_chat_message(content)

    def delete_message(self, data):
        msg_id = int(data['message_id'])
        username = data['sender']
        message = Message.objects.filter(id=msg_id).first()
        if message.user.username == username:
            message.delete()
        messages = Message.objects.filter(room__room_name=data['room'])
        context = {
            "messages": self.messages_to_json(messages),
            "method": "delete_message",
        }
        self.fetch_messages_now(context)

    methods = {
        "fetch_messages": fetch_messages,
        "new_message": new_message,
        "delete_message": delete_message
    }

    def messages_to_json(self, messages):
        return [self.message_to_json(message) for message in messages]

    def message_to_json(self, message):
        return {
            "id": int(message.id),
            "username": message.user.username,
            "body": message.body,
            "room": message.room.room_name,
            "posted_time": f"{message.posted.hour}:{message.posted.minute}"
        }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.methods[data['method']](self, data)
        # message = text_data_json["message"]

    def send_chat_message(self, content):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message",
                "message": content['message'],
                "method": content['method']
            }
        )

    def fetch_messages_now(self, content):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "delete_chat_message",
                "messages": content['messages'],
                "method": content['method']
            }
        )
    def load_messages_to_group(self, messages):
        self.send(text_data=json.dumps(messages))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        method = event["method"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message,
            "method": method
        }))

    def delete_chat_message(self, event):
        messages = event["messages"]
        method = event["method"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "messages": messages,
            "method": method
        }))
