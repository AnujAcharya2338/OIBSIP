import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "system_message",
                "message": f"{self.user.username} has joined the chat",
            }
        )

        history = await self.get_history()
        for msg in history:
            await self.send(text_data=json.dumps({
                "message": msg["content"],
                "username": msg["username"],
                "timestamp": msg["timestamp"],
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "system_message",
                "message": f"{self.user.username} has left the chat",
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        saved = await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": saved["content"],
                "username": saved["username"],
                "timestamp": saved["timestamp"],
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "timestamp": event["timestamp"],
        }))

    async def system_message(self, event):
        await self.send(text_data=json.dumps({
            "system": True,
            "message": event["message"],
        }))

    @database_sync_to_async
    def save_message(self, content):
        room, _ = Room.objects.get_or_create(
            name=self.room_name,
            defaults={"created_by": self.user}
        )
        msg = Message.objects.create(room=room, sender=self.user, content=content)
        return {
            "content": msg.content,
            "username": msg.sender.username,
            "timestamp": msg.timestamp.strftime("%H:%M"),
        }

    @database_sync_to_async
    def get_history(self):
        room, _ = Room.objects.get_or_create(
            name=self.room_name,
            defaults={"created_by": self.user}
        )
        return [
            {
                "content": m.content,
                "username": m.sender.username,
                "timestamp": m.timestamp.strftime("%H:%M"),
            }
            for m in room.messages.all()[:50]
        ]