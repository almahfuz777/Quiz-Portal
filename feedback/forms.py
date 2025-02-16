from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    """
    A form for participants to submit feedback on quizzes.
    """
    class Meta:
        model = Feedback
        fields = ['comment', 'content']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your feedback...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional feedback (optional)...'}),
        }
        labels = {
            'comment': 'Your Feedback',
            'content': 'Additional Comments (Optional)',
        }
