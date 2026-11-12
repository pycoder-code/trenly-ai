from django.core import signing
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from trainers.models import Trainer

TOKEN_SALT = 'trainer-session'
TOKEN_MAX_AGE_SECONDS = 14 * 24 * 60 * 60
INVALID_CREDENTIALS = 'Неверные учётные данные.'


def issue_trainer_token(trainer_id: int) -> str:
    return signing.dumps({'trainer_id': trainer_id}, salt=TOKEN_SALT)


class TrainerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization', '')
        if not header:
            return None
        scheme, _, token = header.partition(' ')
        if scheme != 'Bearer' or not token:
            raise AuthenticationFailed(INVALID_CREDENTIALS)
        try:
            payload = signing.loads(token, salt=TOKEN_SALT, max_age=TOKEN_MAX_AGE_SECONDS)
            trainer = Trainer.objects.get(pk=payload['trainer_id'])
        except (signing.BadSignature, signing.SignatureExpired, Trainer.DoesNotExist, KeyError, TypeError):
            raise AuthenticationFailed(INVALID_CREDENTIALS) from None
        if trainer.status != Trainer.Status.ACTIVE:
            raise AuthenticationFailed(INVALID_CREDENTIALS)
        return (trainer, token)

    def authenticate_header(self, request):
        return 'Bearer'
