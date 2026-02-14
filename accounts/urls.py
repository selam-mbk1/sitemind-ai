from django.urls import path
from . import views

app_name = 'accounts'  # optional but good practice for namespacing

urlpatterns = [
    path('', views.home, name='home'),                   # /accounts/
    path('login/', views.login_view, name='login'),      # /accounts/login/
    path('register/', views.register_view, name='register'),  # /accounts/register/
    path('profile/', views.profile, name='profile'),     # /accounts/profile/
    path('logout/', views.logout_view, name='logout'),  # /accounts/logout/
]
