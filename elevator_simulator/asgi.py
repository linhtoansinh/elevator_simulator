"""
ASGI config for elevator_simulator project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import django

from multiprocessing import AuthenticationError
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevator_simulator.settings')
django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import elevator.urls


#application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(elevator.urls.websocket_urlpatterns)
    )
})