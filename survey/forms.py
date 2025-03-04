from django import forms

class SurveyForm(forms.Form):
    # Fields for clarity of instructions
    clarity_choices = [
        ('Very Clear', 'Very Clear'),
        ('Clear', 'Clear'),
        ('Somewhat Clear', 'Somewhat Clear'),
        ('Unclear', 'Unclear')
    ]
    clarity = forms.ChoiceField(choices=clarity_choices, required=True)

    # Fields for running the interface
    ease_run_choices = [
        ('Very Easy', 'Very Easy'),
        ('Easy', 'Easy'),
        ('Neutral', 'Neutral'),
        ('Difficult', 'Difficult'),
        ('Very Difficult', 'Very Difficult')
    ]
    ease_run = forms.ChoiceField(choices=ease_run_choices, required=True)

    # Fields for providing data
    ease_provide_choices = [
        ('Very Easy', 'Very Easy'),
        ('Easy', 'Easy'),
        ('Neutral', 'Neutral'),
        ('Difficult', 'Difficult'),
        ('Very Difficult', 'Very Difficult')
    ]
    ease_provide = forms.ChoiceField(choices=ease_provide_choices, required=True)

    # Textarea for issues encountered
    issues = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=True)

    # Textarea for suggestions
    suggestions = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=True)

    def clean(self):
        cleaned_data = super().clean()
        # Custom validation if needed
        return cleaned_data
