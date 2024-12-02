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

    If the user has not participated in the quiz, they are redirected 
    with an error message. If feedback has already been submitted, 
    a warning is shown. If the user is allowed to submit feedback, 
    it is saved and a success message is displayed.

    Args:
        request: The HTTP request object.
        quiz_id: The ID of the quiz for which feedback is being submitted.

    Returns:
        Renders the feedback submission page or redirects based on the form submission.
    """
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
    
    # Check if the user has participated in the quiz
    try:
        participant = Participant.objects.get(user=request.user, quiz=quiz)
    except Participant.DoesNotExist:
        messages.error(request, "You must participate in the quiz before submitting feedback.")
        return redirect('quiz_home')
    
    # If the user has already given feedback, prevent multiple submissions
    existing_feedback = Feedback.objects.filter(quiz=quiz, participant=participant).first()
    if existing_feedback:
        messages.warning(request, "You have already submitted feedback for this quiz.")
        return redirect('quiz_home')

    # Handle POST request with valid feedback form
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

    Args:
        request: The HTTP request object.
        quiz_id: The ID of the quiz for which feedback is being viewed.

    Returns:
        Renders the view feedback page, showing all feedback for the quiz.
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
    """
    Displays feedback submitted by the logged-in user for the quizzes they participated in.

    If the user has not participated in any quizzes or has not submitted feedback,
    an appropriate message is displayed.

    Args:
        request: The HTTP request object.

    Returns:
        Renders the my feedback page, showing feedback submitted by the logged-in user.
    """
    # Fetch all participants associated with the logged-in user
    participants = Participant.objects.filter(user=request.user)

    if participants.count() == 0:
        # If no participants found, display a "No feedback" message
        no_feedback_message = "You have not participated in any quizzes."
        return render(request, 'feedback/my_feedback.html', {
            'no_feedback_message': no_feedback_message,
        })
    
    # Fetch all feedbacks associated with the participant(s) for the logged-in user
    feedbacks = Feedback.objects.filter(participant__in=participants).order_by('-created_at')

    # If there are no feedbacks, display a message
    no_feedback_message = "No feedback available for the quizzes you've participated in." if not feedbacks else ""

    return render(request, 'feedback/my_feedback.html', {
        'feedbacks': feedbacks,
        'no_feedback_message': no_feedback_message,
})