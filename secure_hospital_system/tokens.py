from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from .models import SHSUser

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        shs_user = SHSUser.objects.select_related().filter(user = user.id)
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(shs_user[0].email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()
