from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress


class AutoVerifyAccountAdapter(DefaultAccountAdapter):
    """Mark the user's email as verified immediately on signup.

    We don't have an SMTP service, so email verification is disabled and
    every primary email is treated as verified. This unblocks features
    that require a verified email (e.g. MFA activation).
    """

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=commit)
        EmailAddress.objects.filter(user=user).update(verified=True)
        return user
