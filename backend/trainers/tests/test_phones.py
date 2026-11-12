from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from trainers.phones import normalize_phone, validate_phone


class PhoneNormalizationTests(SimpleTestCase):
    def test_leading_eight(self):
        self.assertEqual(normalize_phone('8 999 123-45-67'), '+79991234567')

    def test_plus_seven(self):
        self.assertEqual(normalize_phone('+7 999 123-45-67'), '+79991234567')

    def test_foreign_number_is_rejected(self):
        with self.assertRaises(ValidationError):
            normalize_phone('+1 202 555 0143')

    def test_validator_accepts_russian_number(self):
        validate_phone('8 999 123-45-67')
        validate_phone('+7 999 123-45-67')

    def test_validator_rejects_foreign_number(self):
        with self.assertRaises(ValidationError):
            validate_phone('+1 202 555 0143')

    def test_validator_skips_empty_value(self):
        validate_phone('')
