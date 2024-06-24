from django.urls import path, include
from . import consumers

# the empty string routes to ChatConsumer, which manages the chat functionality.
websocket_urlpatterns = [
    path("/chat", consumers.ChatConsumer.as_asgi()),
]
