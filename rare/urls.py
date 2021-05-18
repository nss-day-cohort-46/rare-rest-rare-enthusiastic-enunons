from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rareapi.views import PostView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostView, 'post')

urlpatterns = [
    path('admin/', admin.site.urls),
]
