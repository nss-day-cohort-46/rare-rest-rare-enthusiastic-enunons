from rest_framework import routers
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rareapi.views import register_user, login_user
from rareapi.views import PostView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostView, 'post')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
