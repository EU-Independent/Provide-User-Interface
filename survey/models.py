from django.db import models

class Question(models.Model):
    CLARITY_CHOICES = [
        ('Very Clear', 'Very Clear'),
        ('Clear', 'Clear'),
        ('Somewhat Clear', 'Somewhat Clear'),
        ('Unclear', 'Unclear'),
    ]

    EASE_CHOICES = [
        ('Very Easy', 'Very Easy'),
        ('Easy', 'Easy'),
        ('Neutral', 'Neutral'),
        ('Difficult', 'Difficult'),
        ('Very Difficult', 'Very Difficult'),
    ]

    question_text = models.CharField(max_length=255)  # The actual question text
    question_type = models.CharField(max_length=50, choices=[
        ('clarity', 'Clarity'),
        ('ease', 'Ease of Use'),
        ('open-ended', 'Open-ended')
    ])  # Type of question (e.g., multiple-choice, text input)

    def __str__(self):
        return self.question_text


class SurveyResponse(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-generated primary key
    issues = models.TextField(default="No issues encountered.")
    suggestions = models.TextField(default="No suggestions provided.")
    
    def __str__(self):
        return f"Survey Response (ID: {self.id})"


class Answer(models.Model):
    survey_response = models.ForeignKey(SurveyResponse, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)  # Store the answer as text

    def __str__(self):
        return f"Answer to '{self.question.question_text}' (Response ID: {self.survey_response.id})"
