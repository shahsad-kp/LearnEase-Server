"""
URL configuration for learn_ease_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include(('Auth.urls', 'Auth'), namespace='Auth')),
    path('api/user/', include(('Users.urls', 'Users'), namespace='Users')),
    path('api/classroom/', include(('ClassRoom.urls', 'ClassRoom'), namespace='ClassRoom')),
    path('api/messages/', include(('Messages.urls', 'Messages'), namespace='Messages')),
    path('api/documents/', include(('Documents.urls', 'Documents'), namespace='Documents')),
    path('api/whiteboard/', include(('Whiteboard.urls', 'Whiteboard'), namespace='Whiteboard')),
    path('api/activities/', include(('Activities.urls', 'Activities'), namespace='Activities')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
