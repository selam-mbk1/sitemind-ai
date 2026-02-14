from django.urls import path
from . import views
from .views import chat_home



app_name = "chat"

urlpatterns = [
    path("", views.chat_home, name="chat_home"),
    path("<int:session_id>/", views.chat_home, name="chat_session"),
]
