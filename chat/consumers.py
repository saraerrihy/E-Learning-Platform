import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user = self.scope['user']
            self.id = self.scope['url_route']['kwargs']['course_id']
            self.room_group_name = f'chat_{self.id}'
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            
            # Send connection message
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': 'Connected to chat room',
                'user': 'System',
                'datetime': timezone.now().isoformat()
            }))
            
        except Exception as e:
            logger.error(f"Error in connect: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            logger.error(f"Error in disconnect: {str(e)}")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            now = timezone.now()

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.user.username,
                    'datetime': now.isoformat(),
                }
            )
        except Exception as e:
            logger.error(f"Error in receive: {str(e)}")
            # Send error message back to sender
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Error processing message: {str(e)}',
                'datetime': timezone.now().isoformat()
            }))

    async def chat_message(self, event):
        try:
            # Send message to WebSocket
            await self.send(text_data=json.dumps(event))
        except Exception as e:
            logger.error(f"Error in chat_message: {str(e)}")

