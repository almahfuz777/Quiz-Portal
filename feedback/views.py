from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback
from .forms import FeedbackForm
from quiz.models import Quiz
from participation.models import Participant

@login_required
def submit_feedback(request, quiz_id):
    """
    Handles feedback submission for a quiz by a participant.
    """
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
    
    # Check if the user has participated in the quiz
    try:
        participant = Participant.objects.get(user=request.user, quiz=quiz)
    except Participant.DoesNotExist:
        # If no participant found, show an alert message and redirect
        messages.error(request, "You must participate in the quiz before submitting feedback.")
        return redirect('quiz_home')
    
    # If the user has already given feedback, prevent multiple submissions
    existing_feedback = Feedback.objects.filter(quiz=quiz, participant=participant).first()
    if existing_feedback:
        messages.warning(request, "You have already submitted feedback for this quiz.")
        return redirect('quiz_home')

    # If it's a POST request, handle the form submission
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.quiz = quiz
            feedback.participant = participant
            feedback.save()
            messages.success(request, "Your feedback has been submitted successfully!")
            return redirect('quiz_home')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/submit_feedback.html', {'quiz': quiz, 'form': form})


@login_required
def view_feedback(request, quiz_id):
    """
    Displays all feedbacks for a specific quiz (from all participants).
    """
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
    
    # Fetch all feedbacks for the given quiz
    feedbacks = Feedback.objects.filter(quiz=quiz).order_by('-created_at')

    # If no feedbacks exist for the quiz, show the message
    no_feedback_message = "No feedback available for this quiz." if not feedbacks else ""

    return render(request, 'feedback/view_feedback.html', {
        'feedbacks': feedbacks,
        'quiz': quiz,
        'no_feedback_message': no_feedback_message,
    })


@login_required
def my_feedback(request):
    # Fetch all participants associated with the logged-in user
    participants = Participant.objects.filter(user=request.user)

    if participants.count() == 0:
        # If no participants found, we can display a "No feedback" message
        no_feedback_message = "You have not participated in any quizzes."
        return render(request, 'feedback/view_feedback.html', {
            'no_feedback_message': no_feedback_message,
        })
    
    # Fetch all feedbacks associated with the participant(s) for the logged-in user
    feedbacks = Feedback.objects.filter(participant__in=participants).order_by('-created_at')

    # If there are no feedbacks, display a message
    no_feedback_message = "No feedback available for the quizzes you've participated in." if not feedbacks else ""

    return render(request, 'feedback/view_feedback.html', {
        'feedbacks': feedbacks,
        'no_feedback_message': no_feedback_message,
    })
