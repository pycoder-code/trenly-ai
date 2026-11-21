"""Проверка, что процесс отвечает."""

from django.http import JsonResponse


def health(request):
    """Ответ, что приложение живо."""
    return JsonResponse({'status': 'ok'})
