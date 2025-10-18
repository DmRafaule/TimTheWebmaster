from django.urls import reverse

from allauth.account.adapter import DefaultAccountAdapter


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
