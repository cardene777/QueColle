from django.contrib.auth import forms as auth_forms


class LoginForm(auth_forms.AuthenticationForm):
    """
    login form
    """

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class SignUpForm(auth_forms.UserCreationForm):
    """
    signup form
    """

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
