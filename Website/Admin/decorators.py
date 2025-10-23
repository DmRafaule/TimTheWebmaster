from django.urls import reverse_lazy
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

def superuser_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_name='login'
):
    """
    Decorator for views that checks that the user is logged in and it is a superuser, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(is_superuser, reverse_lazy(login_name), redirect_field_name)
    if function:
        return actual_decorator(function)
    return actual_decorator