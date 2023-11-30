# chat/routing.py
from django.urls import path

from .consumers import SepulkaCreateConsumer

websocket_urlpatterns = [
    path('ws/create/', SepulkaCreateConsumer.as_asgi()),
]