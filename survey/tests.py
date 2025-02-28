from django.test import TestCase
from .models import SurveyResponse

class SurveyResponseTest(TestCase):
    def setUp(self):
        SurveyResponse.objects.create(
            user="test_user",
            clarity="Clear",
            ease_run="Easy",
            ease_provide="Neutral",
            issues="No major issues.",
            suggestions="More documentation."
        )

    def test_survey_response_creation(self):
        response = SurveyResponse.objects.get(user="test_user")
        self.assertEqual(response.clarity, "Clear")
        self.assertEqual(response.ease_run, "Easy")
        self.assertEqual(response.ease_provide, "Neutral")
