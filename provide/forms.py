# forms.py

from django import forms
from django.core.exceptions import ValidationError

class UploadMetadataForm(forms.Form):
    offer_title = forms.CharField()
    offer_description = forms.CharField()
    keywords = forms.CharField()
    offer_publisher = forms.CharField()
    offer_language = forms.CharField()
    offer_license = forms.ChoiceField(choices=[])
    accessUrl = forms.URLField()
    start = forms.DateTimeField()
    end = forms.DateTimeField()
    value = forms.CharField(widget=forms.Textarea)
    # Authentication fields for access URL testing and artifact creation
    AUTH_TYPE_CHOICES = (
        ('none', 'None'),
        ('basic', 'Basic (username/password)'),
        ('bearer', 'Bearer (token)'),
    )
    auth_type = forms.ChoiceField(choices=AUTH_TYPE_CHOICES, required=False, initial='none')
    auth_username = forms.CharField(required=False)
    auth_password = forms.CharField(required=False, widget=forms.PasswordInput)
    auth_token = forms.CharField(required=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        license_choices = kwargs.pop('license_choices', [])
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['offer_license'].choices = license_choices

    def clean(self):
        cleaned = super().clean()
        auth_type = cleaned.get('auth_type')
        if auth_type == 'basic':
            if not cleaned.get('auth_username') or not cleaned.get('auth_password'):
                raise ValidationError('Username and password are required for basic authentication')
        if auth_type == 'bearer':
            if not cleaned.get('auth_token'):
                raise ValidationError('Token is required for bearer authentication')
        return cleaned

    def clean_accessUrl(self):
        url = self.cleaned_data.get('accessUrl')
        if url and self.request and url.startswith('/'):
            url = self.request.build_absolute_uri(url)
        return url