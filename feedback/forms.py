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
