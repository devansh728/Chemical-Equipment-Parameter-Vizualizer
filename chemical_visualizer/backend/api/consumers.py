import json
from channels.generic.websocket import AsyncWebsocketConsumer


class AnalysisConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time analysis notifications.
    """
    
    async def connect(self):
        """
        Handle WebSocket connection.
        Authenticate user and add to their specific group.
        """
        user = self.scope.get('user')
        
        # Accept both authenticated and unauthenticated users (for development)
        if user and user.is_authenticated:
            self.user = user
            self.group_name = f"user_{user.id}"
        else:
            # For unauthenticated users, use a broadcast group
            self.user = None
            self.group_name = "broadcast_group"
        
        # Add this connection to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.
        Remove from user group.
        """
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """
        Handle messages received from WebSocket.
        This can be used for ping/pong or other client messages if needed.
        """
        pass
    
    async def analysis_message(self, event):
        """
        Handler called by Celery task to send analysis updates to the client.
        This is triggered by channel_layer.group_send().
        """
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

