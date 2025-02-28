from django import forms
from .models import SurveyResponse

class SurveyForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        fields = ['issues', 'suggestions']  # Only include fields present in SurveyResponse
        widgets = {
            'issues': forms.Textarea(attrs={'rows': 4}),
            'suggestions': forms.Textarea(attrs={'rows': 4}),
        }
