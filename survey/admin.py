from django.contrib import admin
from .models import SurveyResponse, Question, Answer

# Register the Question model
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type')
    search_fields = ('question_text',)
    list_filter = ('question_type',)

admin.site.register(Question, QuestionAdmin)

# Register the SurveyResponse model
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'issues', 'suggestions')
    search_fields = ('issues', 'suggestions')
    list_filter = ('issues',)

admin.site.register(SurveyResponse, SurveyResponseAdmin)

# Register the Answer model
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('survey_response', 'question', 'answer_text')
    search_fields = ('answer_text',)
    list_filter = ('question',)

admin.site.register(Answer, AnswerAdmin)
