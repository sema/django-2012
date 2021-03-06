
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from registration.backends.simple import RegistrationForm as BaseRegistrationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class AuthenticationForm(BaseAuthenticationForm):

    helper = FormHelper()
    helper.add_input(Submit('login', _(u'Log in')))

class RegistrationForm(BaseRegistrationForm):

    helper = FormHelper()
    helper.add_input(Submit('register', _(u'Register')))