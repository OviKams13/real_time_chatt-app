from django.urls import path
from .consumers import ChatConsumer

wsPattern = [
    path("ws/messages/<str:roomN_pk>/", ChatConsumer.as_asgi())
]