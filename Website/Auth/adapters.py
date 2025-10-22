from django.urls import reverse

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_pk_to_url_str, url_str_to_user_pk


class MyAccountAdapter(DefaultAccountAdapter):

    confirmation_view_name = "email_verify_with_code"

    def get_email_confirmation_url(self, request, emailconfirmation):
        # Customize the URL, e.g. point to a custom frontend route
        domain = request.get_host()
        relative_url = reverse(self.confirmation_view_name, kwargs={
            'verification_code': emailconfirmation.key
            })
        url = f"https://{domain}{relative_url}"
        return url

    def get_reset_password_from_key_url(self, key):
        uidb36 = key.split('-')[0]
        key_hash = f"{key.split('-')[1]}-{key.split('-')[2]}" 
        protocol = "https" if self.request.is_secure() else "http" # Используйте 'http' для разработки
        relative_url = reverse(
            "account_reset_password_from_key",
            kwargs={"uidb36": uidb36, "key": key_hash}
        )

        # 3. Собираем абсолютный URL (протокол + домен + относительный URL)
        domain = self.request.get_host()
        url = f"{protocol}://{domain}{relative_url}"
        return url