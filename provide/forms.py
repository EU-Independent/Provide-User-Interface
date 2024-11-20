from django import forms
 

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
    offer_license = forms.CharField()
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
    accessUrl = forms.URLField()
    #automatedDownload = forms.ChoiceField(choices=[('True', 'True'), ('False', 'False')])



    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start")
        end_date = cleaned_data.get("end")

        if start_date and end_date and end_date < start_date:
            raise ValidationError("End date cannot be before the start date.")
        
        return cleaned_data