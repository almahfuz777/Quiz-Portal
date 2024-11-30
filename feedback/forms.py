"""
A form for submitting feedback related to a specific quiz.

    This form is linked to the Feedback model and includes fields for:
    - `comment`: The main feedback text (required).
    - `content`: Additional optional details (optional).

"""
from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback # Associate the form with the Feedback model
        fields = ['quiz', 'participant', 'comment', 'content']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Write your main feedback here...'}), # Placeholder to guide user input
            'content': forms.Textarea(attrs={'placeholder': 'Additional details (optional)...'}), # Placeholder for optional content
        }
