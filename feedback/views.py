from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback
from quiz.models import Quiz, Participant
from .forms import FeedbackForm
from django.core.exceptions import ObjectDoesNotExist


# @login_required
def view_feedbacks(request, quiz_id,participant_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    participant = get_object_or_404(Participant, id=participant_id)
    feedbacks = Feedback.objects.filter(quiz=quiz).order_by('-created_at')

    user_participant = None
    if request.user.is_authenticated:
        try:
            user_participant = Participant.objects.get(user=request.user, quiz=quiz)
        except Participant.DoesNotExist:
            pass  # Handle gracefully if the user has not participated

    return render(request, 'feedback/view_feedback.html', {
        'quiz': quiz,
        'feedbacks': feedbacks,
        'participant': user_participant,  # Pass the logged-in user's participant object
    })


# @login_required
def submit_feedback(request, quiz_id, participant_id):
    """Allow a participant to submit feedback for a quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id)

    participant = get_object_or_404(Participant, id=participant_id)
    
    


    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.quiz = quiz
            feedback.participant = participant
            feedback.save()
            return redirect('view_feedbacks', quiz_id=quiz.id,participant_id=participant.id)  # Redirect to the feedback  view
    else:
        form = FeedbackForm()

    return render(request, 'feedback/submit_feedback.html', {
        'quiz': quiz, 
        'form': form,
        'participant':participant,
        })
