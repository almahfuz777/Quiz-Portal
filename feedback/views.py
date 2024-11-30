from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback
from quiz.models import Quiz, Participant
from .forms import FeedbackForm
from django.core.exceptions import ObjectDoesNotExist



# View to display all feedbacks for a specific quiz
@login_required
def view_feedbacks(request, quiz_id, participant_id):
    """
    Displays all feedbacks for a specific quiz.
    
    Parameters:
        request: The HTTP request object.
        quiz_id (int): The ID of the quiz for which feedbacks are retrieved.
        participant_id (int): The ID of the participant viewing the feedbacks.

    Returns:
        HTTPResponse: Renders the feedback viewing template with feedback data.
    """
    # Fetch the quiz object, or return a 404 if not found
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)

    # Fetch the participant object, or return a 404 if not found
    participant = get_object_or_404(Participant, id=participant_id, user=request.user, quiz=quiz)

    # Retrieve all feedbacks for the specified quiz, ordered by creation date
    feedbacks = Feedback.objects.filter(quiz=quiz).order_by('-created_at')

    user_participant = None
    if request.user.is_authenticated:
        try:
            # Attempt to retrieve the participant object for the logged-in user
            user_participant = Participant.objects.get(user=request.user, quiz=quiz)
        except Participant.DoesNotExist:
            # Handle the case where the logged-in user has not participated in the quiz
            user_participant = None  # Set to None explicitly
            print(f"User {request.user.username} has not participated in this quiz.")

    return render(request, 'feedback/view_feedback.html', {
        'quiz': quiz,
        'feedbacks': feedbacks,
        'participant': user_participant,  # Include the logged-in user's participant object
    })


@login_required
def submit_feedback(request, quiz_id, participant_id):
    """
    Allows a participant to submit feedback for a quiz.

    Parameters:
        request: The HTTP request object.
        quiz_id (uuid): The ID of the quiz being reviewed.
        participant_id (int): The ID of the participant submitting the feedback.

    Returns:
        HTTPResponse: Renders the feedback submission form or redirects after successful submission.
    """
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
    
    # Get the participant object based on participant_id and ensure it is linked to the logged-in user
    participant = get_object_or_404(Participant, id=participant_id, user=request.user, quiz=quiz)

    # If the request method is POST, handle the form submission
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.quiz = quiz
            feedback.participant = participant
            feedback.save()
            return redirect('view_feedbacks', quiz_id=str(quiz.quiz_id), participant_id=participant.id)
    else:
        form = FeedbackForm()

    return render(request, 'feedback/submit_feedback.html', {'quiz': quiz, 'form': form})