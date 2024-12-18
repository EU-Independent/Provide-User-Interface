from django import forms
from django.core.exceptions import ValidationError

class UploadMetadataForm(forms.Form):
    #catalog_title = forms.CharField()
    #catalog_description = forms.CharField()
    #representation_title = forms.CharField()
    #representation_description = forms.CharField()
    #language = forms.CharField()
    #mediaType = forms.CharField()
    offer_title = forms.CharField()
    offer_description = forms.CharField()
    keywords = forms.CharField()
    offer_publisher = forms.CharField()
    offer_language = forms.CharField()
    offer_license = forms.ChoiceField(choices=[])  # Dynamic choices populated at runtime
    accessUrl = forms.URLField()
    #paymentMethod = forms.CharField()
    #contract_title = forms.CharField()
    #contract_description = forms.CharField()
    start = forms.DateTimeField()
    end = forms.DateTimeField()
    #rule_title = forms.CharField()
    #rule_description = forms.CharField()
    value = forms.CharField(widget=forms.Textarea)
    #artifact_title = forms.CharField()
    #artifact_description = forms.CharField()
    #automatedDownload = forms.ChoiceField(choices=[('True', 'True'), ('False', 'False')])

    def __init__(self, *args, **kwargs):
        license_choices = kwargs.pop('license_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['offer_license'].choices = license_choices