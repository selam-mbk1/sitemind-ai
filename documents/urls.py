from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path('', views.documents_home, name='documents_home'),
    path('upload/', views.upload_document, name='upload'),
]
