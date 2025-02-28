from django.contrib import admin
from .models import Question, SurveyResponse, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1  # Number of extra empty forms to display in the admin

class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'issues', 'suggestions']
    search_fields = ['id', 'issues', 'suggestions']
    inlines = [AnswerInline]  # Include answers inline with the survey response

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_type']
    search_fields = ['question_text', 'question_type']
    list_filter = ['question_type']  # Allow filtering by question type

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['survey_response', 'question', 'answer_text']
    search_fields = ['survey_response__id', 'question__question_text', 'answer_text']
    list_filter = ['question__question_type']  # Allow filtering by question type

# Register models with the admin site
admin.site.register(SurveyResponse, SurveyResponseAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
