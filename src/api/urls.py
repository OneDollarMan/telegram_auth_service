from django.urls import path
from .views import GenerateTokenView, RegisterUserView, AuthenticateAndLoginView, get_index, LogoutView

urlpatterns = [
    path('', get_index, name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('generate_token/', GenerateTokenView.as_view(), name='generate_token'),
    path('register_user/', RegisterUserView.as_view(), name='register_user'),
    path('auth_user/', AuthenticateAndLoginView.as_view(), name='authenticate_and_login'),
]