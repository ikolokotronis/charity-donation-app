from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        token_value = (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))
        return token_value


token_generator = AppTokenGenerator()
