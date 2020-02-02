from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib import messages
from django.contrib.auth import logout, password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.files.images import get_image_dimensions
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext as _

from core.models import Profile, Balances


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')


class UserProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=False)
    avatar = forms.ImageField(required=False)
    SEX_CHOICES = (
        ('m', u"남성"),
        ('w', u"여성"),
    )
    sex = forms.ChoiceField(label=u'성별', choices=SEX_CHOICES)

    class Meta:
        model = Profile
        fields = ['avatar', 'nickname', 'sex']

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if avatar:
            try:
                w, h = get_image_dimensions(avatar)

                main, sub = avatar.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                    raise forms.ValidationError(_('Please use a JPEG, '
                                                  'GIF or PNG image.'))

            except AttributeError:
                """
                Handles case when we are updating the user profile
                and do not supply a new avatar
                """
                pass

        return avatar


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    email = forms.CharField(
        label=_("Email"),
        strip=False,
        widget=forms.EmailInput
    )
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    nickname = forms.CharField(max_length=16)
    # is_want_staff = forms.BooleanField(required=False)
    phone = forms.CharField(required=False)
    SEX_CHOICES = (
        ('m', u"남성"),
        ('w', u"여성"),
    )
    sex = forms.ChoiceField(label=u'성별', choices=SEX_CHOICES)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'class': 'validate'}, api_params={'hl': 'ko'}))

    class Meta:
        model = User
        fields = ("username", "captcha")
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        Balances.objects.create(user=user, type_id=1).save()
        return user


class CustomLoginForm(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('main_page')

    template_name = 'user/login.html'

    def form_valid(self, form):
        user = form.get_user()
        AuthenticationForm.confirm_login_allowed(form, user=user)
        return super(CustomLoginForm, self).form_valid(form)

    def form_invalid(self, form):
        return super(CustomLoginForm, self).form_invalid(form)


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect(reverse('core:main_page'))
