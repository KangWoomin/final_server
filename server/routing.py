from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from streaming.consumers import StreamConsumer
from channels.auth import AuthMiddlewareStack


websocket_urlpatterns = [
    path("ws/stream/", StreamConsumer.as_asgi()),  # 경로와 Consumer를 정의하세요.
]

application = ProtocolTypeRouter({
    # 다른 프로토콜에 대한 라우팅을 설정할 수 있습니다.
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)  # URLRouter에 URL 목록을 전달
    ),
})