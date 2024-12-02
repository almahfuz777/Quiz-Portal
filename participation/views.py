from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from quiz.models import Quiz, Question, QuizStats
from .models import Participant, Response

@login_required
def participate(request, quiz_id):
    """
    Handles participation in a quiz. Ensures that the quiz is active and the user
    has not already participated. If the quiz is active and the user has not participated,
    it renders the quiz participation form.
    
    Args:
        request: The HTTP request object.
        quiz_id: The unique identifier for the quiz.

    Returns:
        A rendered response containing the quiz participation interface or a redirection to
        the quiz home page if the quiz has expired or the user has already participated.
    """
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)

    # Ensure the quiz is active
    if not quiz.is_active():
        messages.error(request, "This quiz has expired.")
        return redirect('quiz_home')

    # Check if the user has already participated
    participant = Participant.objects.filter(user=request.user, quiz=quiz).first()
    if participant:
        messages.warning(request, "You have already participated in this quiz.")
        return redirect('quiz_home')

    # If it's a private quiz, verify the password
    if quiz.quiz_type == 'private':
        if request.method == 'POST' and 'password' in request.POST:
            provided_password = request.POST['password']
            if not quiz.check_password(provided_password):
                messages.error(request, "Incorrect password. Please try again.")
                return redirect('participate', quiz_id=quiz.quiz_id)
        elif request.method == 'GET' or 'password' not in request.POST:
            return render(request, 'participation/private_quiz_verification.html', {
                'quiz': quiz
            })

    # If it's a POST request, handle quiz submission
    if request.method == 'POST' and 'password' not in request.POST:
        return submit_quiz(request, quiz)

    questions = quiz.questions.all()
    duration_in_seconds = int(quiz.duration.total_seconds())

    return render(request, 'participation/participate.html', {
        'quiz': quiz,
        'questions': questions,
        'duration_in_seconds': duration_in_seconds,
    })


@login_required
def submit_quiz(request, quiz):
    """
    Processes the quiz submission and calculates the participant's score. It creates or retrieves
    a participant record, saves the responses, calculates the raw and percentage score, and updates
    quiz statistics.

    Args:
        request: The HTTP request object.
        quiz: The quiz object that the user is participating in.

    Returns:
        A rendered response displaying the result page with the raw score, percentage score,
        and quiz statistics.
    """
    user = request.user
    participant, created = Participant.objects.get_or_create(
        user=user, quiz=quiz, defaults={"start_time": now()}
    )

    # Prevent duplicate submissions
    if not created and participant.end_time:
        messages.error(request, "You have already submitted this quiz.")
        return redirect('quiz_home')

    # Calculate raw score and responses
    questions = quiz.questions.all()
    total_questions = questions.count()
    raw_score = 0
    responses = []

    for question in questions:
        selected_option = request.POST.get(f"selected_option_{question.question_no}")
        is_correct = selected_option == question.correct_option
        if is_correct:
            raw_score += 1  # Increment raw score for correct answers
        responses.append(Response(
            participant=participant,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct
        ))

    # Save responses and update participant score
    Response.objects.bulk_create(responses)
    percentage_score = (raw_score / total_questions) * 100  # Calculate score as a percentage
    participant.score = percentage_score
    participant.end_time = now()
    participant.save()

    # Update quiz stats
    quiz_stats, _ = QuizStats.objects.get_or_create(quiz=quiz)
    all_scores = quiz.participants.values_list('score', flat=True)
    quiz_stats.update_stats(all_scores)

    # Render the result page
    return render(request, 'participation/result.html', {
        "quiz": quiz,
        "raw_score": raw_score,  # Raw score
        "percentage_score": percentage_score,  # Percentage score
        "total_questions": total_questions,
        "participant": participant,
        "quiz_stats": quiz_stats,
    })


@login_required
def quiz_info(request, quiz_id):
    """
    Displays detailed information about a specific quiz, including its title, description, 
    formatted duration, and associated statistics. The function calculates the duration in a
    human-readable format and retrieves the quiz statistics.

    Args:
        request: The HTTP request object.
        quiz_id: The unique identifier for the quiz.

    Returns:
        A rendered response containing the quiz information, including duration and statistics.
    """
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)

    # Format duration
    def format_duration(duration):
        """
        Converts the duration of the quiz from timedelta format to a human-readable string.
        
        Args:
            duration: The duration of the quiz in timedelta format.
        
        Returns:
            A formatted string representing the duration in hours, minutes, and seconds.
        """
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        return f"{minutes}m {seconds}s"

    # Retrieve quiz statistics
    quiz_stats = QuizStats.objects.filter(quiz=quiz).first()

    # Prepare quiz data for rendering
    context = {
        "quiz": quiz,
        "formatted_duration": format_duration(quiz.duration),
        "quiz_stats": quiz_stats,  # Pass quiz stats to the template
    }
    return render(request, "participation/quiz_info.html", context)

