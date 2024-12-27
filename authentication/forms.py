import logging

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core import exceptions
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger('django')

class LoginForm(AuthenticationForm):
    error_messages = { 'invalid_login': _('Invalid login'), 'inactive': _('Inactive'), }
    def confirm_login_allowed(self, user):
        logger.info(f"Login failed for inactive user: {user.username}")
        if not user.is_active: raise exceptions.ValidationError(self.error_messages['inactive'], code='inactive')
