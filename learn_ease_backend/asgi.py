"""
ASGI config for learn_ease_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.layers import get_channel_layer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.core.asgi import get_asgi_application

from Auth.middleware import JwtAuthMiddlewareStack
from learn_ease_backend.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learn_ease_backend.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': OriginValidator(
            JwtAuthMiddlewareStack(
                URLRouter(
                    routes=websocket_urlpatterns
                )
            ),
            ['localhost:5173', '10.4.2.254:5173', '*']
        )
    }
)

application = ASGIStaticFilesHandler(application)

channel_layer = get_channel_layer()
