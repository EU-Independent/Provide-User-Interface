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

    def __init__(self, *args, **kwargs):
        license_choices = kwargs.pop('license_choices', [])
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['offer_license'].choices = license_choices

    def clean_accessUrl(self):
        url = self.cleaned_data.get('accessUrl')
        if url and self.request and url.startswith('/'):
            url = self.request.build_absolute_uri(url)
        return url