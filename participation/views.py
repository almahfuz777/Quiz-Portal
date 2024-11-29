from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from quiz.models import Quiz, Question, QuizStats
from .models import Participant, Response

@login_required
def participate(request, quiz_id):
    """Handles participation in a quiz."""
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

    # If it's a POST request, handle quiz submission
    if request.method == 'POST':
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
    """Processes quiz submission and calculates scores."""
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
