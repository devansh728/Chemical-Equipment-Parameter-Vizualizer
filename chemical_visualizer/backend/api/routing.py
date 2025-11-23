from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/analysis/', consumers.AnalysisConsumer.as_asgi()),
]

