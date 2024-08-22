from django.forms import CharField, EmailField, Form, PasswordInput, TextInput, ValidationError
from django.contrib.auth.models import User


def widget_attrs(placeholder):
    return {"class": "u-full-width", "placeholder": placeholder}


def form_kwargs(widget, label="", max_length=64):
    return {"widget": widget, "label": label, "max_length": max_length}


class LoginForm(Form):

    username = CharField(**form_kwargs(widget=TextInput(attrs=widget_attrs("Username"))))
    password = CharField(**form_kwargs(widget=PasswordInput(attrs=widget_attrs("Password"))))

    def clean(self):
        if self.errors:
            return self.cleaned_data

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
            raise ValidationError("Incorrect username and/or password.")

        return self.cleaned_data


class RegistrationForm(Form):

    username = CharField(**form_kwargs(widget=TextInput(attrs=widget_attrs("Username"))))
    email = EmailField(**form_kwargs(widget=TextInput(attrs=widget_attrs("Email"))))
    password = CharField(**form_kwargs(widget=PasswordInput(attrs=widget_attrs("Password"))))
    password_confirmation = CharField(**form_kwargs(widget=PasswordInput(attrs=widget_attrs("Confirm your password"))))

    def clean(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")

        if password and password != password_confirmation:
            raise ValidationError("Passwords don't match.")

        return self.cleaned_data
