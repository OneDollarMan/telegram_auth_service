from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserToken


def create_user_token():
    user_token = UserToken()
    user_token.save()
    user_token.refresh_from_db()
    return user_token.id


def register_user_with_username(token, username):
    if not username:
        raise ValidationError("Username is required.")

    user_token = UserToken.objects.get(id=token, username=None)
    if not user_token:
        raise ValidationError("No user_id found")

    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username)

    user_token.username = username
    user_token.save()

    return True


def auth_user_by_id(request, token_id):
    try:
        token = UserToken.objects.get(id=token_id)
    except UserToken.DoesNotExist:
        return False

    try:
        user = User.objects.get(username=token.username)
    except User.DoesNotExist:
        return False

    login(request, user)
    token.delete()
    return True