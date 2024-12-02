import jwt
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from .service import create_user_token, register_user_with_username, auth_user_by_id
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def get_index(request):
    """Страница с кнопкой 'Войти через Telegram'."""
    return render(request, 'index.html', context={"TELEGRAM_BOT_NAME": settings.TELEGRAM_BOT_NAME})


class LogoutView(APIView):

    def get(self, request):
        logout(request)
        return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)


class GenerateTokenView(APIView):
    """
    Генерация уникального токена и редирект в Telegram-бота.
    """
    def get(self, request):
        token = create_user_token()
        return Response({"token": token}, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    """
    Обрабатывает POST-запрос с JWT, раскодирует его и регистрирует пользователя.
    """
    def post(self, request):
        try:
            token = request.data.get('token')
            if not token:
                raise ValidationError("JWT token is required")

            decoded_payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            res = register_user_with_username(decoded_payload['token'], decoded_payload['username'])
            return Response({"res": res}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({"error": "JWT token has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid JWT token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuthenticateAndLoginView(APIView):
    """
    Авторизует пользователя по ID из модели UserToken и производит авторизацию.
    """
    def post(self, request):
        try:
            token_id = request.data.get('id')
            if not token_id:
                raise ValidationError("ID is required")

            if auth_user_by_id(request, token_id):
                return Response({"message": "Authentication successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)