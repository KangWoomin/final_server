from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from streaming.consumers import StreamConsumer
from channels.auth import AuthMiddlewareStack


websocket_urlpatterns = [
    path("ws/stream/", StreamConsumer.as_asgi()), 
]

application = ProtocolTypeRouter({

    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns) 
    ),
})