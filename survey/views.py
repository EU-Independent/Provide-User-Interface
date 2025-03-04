from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SurveyForm
from .models import SurveyResponse



def survey_view(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            # Save the survey response
            response = form.save(commit=True)
            response.save()
            
            messages.success(request, "Thank you for completing the survey!")
            return redirect('survey')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SurveyForm()

    return render(request, 'survey/survey.html', {'form': form})

