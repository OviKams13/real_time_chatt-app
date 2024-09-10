import json #to parse the JSON response from the API.
from channels.generic.websocket import AsyncWebsocketConsumer #to handle websocket connexion.
from channels.db import database_sync_to_async #to interact with the Django database in an asynchronous context.
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_room = f"room_{self.scope['url_route']['kwargs']['roomN_pk']}"
        await self.channel_layer.group_add(self.chat_room, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chat_room, self.channel_name)
        self.close(code)

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        event = {"type": "send_message", "message": data_json}

        await self.channel_layer.group_send(self.chat_room, event)

    async def send_message(self, event):
        data = event["message"]
        await self.create_message(data=data)

        response = {"sender": data["sender"], "message": data["message"]}

        await self.send(text_data=json.dumps({"message": response}))

    @database_sync_to_async
    def create_message(self, data):
        get_room = Room.objects.get(room_name=data["room_name"])

        if not Message.objects.filter(
            message=data["message"], sender=data["sender"]
        ).exists():
            new_message = Message.objects.create(
                room=get_room, message=data["message"], sender=data["sender"]
            )
