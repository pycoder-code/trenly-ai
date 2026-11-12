import re

from django.core.exceptions import ValidationError

_SEPARATORS = re.compile(r'[\s()\-]')


def normalize_phone(value: str) -> str:
    """Приводит российский номер к виду +7 и десять цифр."""
    if value is None or not str(value).strip():
        raise ValidationError('Укажите телефон.')
    compact = _SEPARATORS.sub('', str(value).strip())
    if compact.startswith('+'):
        digits = compact[1:]
    else:
        digits = compact
        if len(digits) == 11 and digits.startswith('8'):
            digits = '7' + digits[1:]
    if not digits.isdigit() or len(digits) != 11 or not digits.startswith('7'):
        raise ValidationError('Телефон должен быть российским номером.')
    return f'+{digits}'


def validate_phone(value: str) -> None:
    """Проверяет, что значение — российский номер. Пустое значение не проверяет."""
    if value is None or not str(value).strip():
        return
    normalize_phone(value)
