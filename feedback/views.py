from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback
from quiz.models import Quiz, Participant
from .forms import FeedbackForm
from django.core.exceptions import ObjectDoesNotExist

# View to display all feedbacks for a specific quiz
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
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Fetch the participant object, or return a 404 if not found
    participant = get_object_or_404(Participant, id=participant_id)

    # Retrieve all feedbacks for the specified quiz, ordered by creation date
    feedbacks = Feedback.objects.filter(quiz=quiz).order_by('-created_at')

    user_participant = None
    if request.user.is_authenticated:
        try:
            # Attempt to retrieve the participant object for the logged-in user
            user_participant = Participant.objects.get(user=request.user, quiz=quiz)
        except Participant.DoesNotExist:
            pass  # Safely handle cases where the user has not participated in the quiz

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
        quiz_id (int): The ID of the quiz being reviewed.
        participant_id (int): The ID of the participant submitting the feedback.

    Returns:
        HTTPResponse: Renders the feedback submission form or redirects after successful submission.
    """
    # Fetch the quiz object, or return a 404 if not found
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Fetch the participant object, or return a 404 if not found
    participant = get_object_or_404(Participant, id=participant_id)

    if request.method == 'POST':  # Check if the form is submitted
        form = FeedbackForm(request.POST)  

        if form.is_valid():  # Validate the form
            feedback = form.save(commit=False)  # Create a feedback object without saving to the database
            feedback.quiz = quiz  
            feedback.participant = participant  
            feedback.save()  # Save the feedback to the database

            # Redirect to the feedback view page after successful submission
            return redirect('view_feedbacks', quiz_id=quiz.id, participant_id=participant.id)
        else:
            # Log form errors for debugging (can be improved with proper logging)
            print("Form errors:", form.errors)
    else:
        form = FeedbackForm()  # Initialize an empty form for GET requests

    
    return render(request, 'feedback/submit_feedback.html', {
        'quiz': quiz, 
        'form': form,
        'participant': participant,
    })
