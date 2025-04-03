from django.urls import path
from .views.index_view import index
from .consumers.elevator_consumer import ElevatorConsumer

urlpatterns = [
    path('', index, name='index'),
]

websocket_urlpatterns = [
    path('ws/elevators/', ElevatorConsumer.as_asgi())
]