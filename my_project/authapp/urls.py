from authapp.apps import AuthappConfig
from django.urls import path
from authapp import views


app_name = AuthappConfig.name

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('edit/', views.EditProfileView.as_view(), name='profile_edit'),
]