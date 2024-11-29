from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from datetime import timedelta, datetime
from django.utils.timezone import make_aware
from .models import Quiz, Question, Participant

@login_required
def quiz_home(request):
    quizzes = Quiz.objects.filter(expiry_date__gt=now())  # Filter active quizzes
    quiz_type = request.GET.get('quiz_type')
    tag = request.GET.get('tag')
    
    if quiz_type:
        quizzes = quizzes.filter(quiz_type=quiz_type)
    if tag:
        quizzes = quizzes.filter(tags__icontains=tag)
    
        # Format duration into a readable format
    for quiz in quizzes:
        # Convert the duration (timedelta) to hours, minutes, seconds
        duration_seconds = int(quiz.duration.total_seconds())
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        seconds = duration_seconds % 60
        quiz.formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
        
    return render(request, 'quiz/quiz_home.html', {'quizzes': quizzes})

@login_required
def create_quiz(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        quiz_type = request.POST.get('quiz_type')
        password = request.POST.get('password') if quiz_type == 'private' else None
        duration_hours = int(request.POST.get('duration_hours', 0))
        duration_minutes = int(request.POST.get('duration_minutes', 0))
        duration_seconds = int(request.POST.get('duration_seconds', 0))
        expiry_date = request.POST.get('expiry_date')
        tags = request.POST.get('tags')
        can_view_score = request.POST.get('can_view_score') == 'on'

        # Validate duration and expiry_date formats
        try:
            duration_timedelta = timedelta(hours=duration_hours, minutes=duration_minutes, seconds=duration_seconds)
        except ValueError:
            return HttpResponse("Invalid duration format.", status=400)

        try:
            expiry_date = make_aware(datetime.strptime(expiry_date, "%Y-%m-%dT%H:%M"))
        except ValueError:
            return HttpResponse("Invalid expiry date format.", status=400)

        quiz = Quiz.objects.create(
            title=title,
            description=description,
            quiz_type=quiz_type,
            password=password,
            duration=duration_timedelta,
            expiry_date=expiry_date,
            tags=tags,
            can_view_score_immediately=can_view_score,
            created_by=request.user,  # Associate the quiz with the user
        )
        messages.success(request, f'Quiz "{quiz.title}" created successfully. Now, you can set questions.')
        return redirect('set_questions', quiz_id=quiz.id)

    return render(request, 'quiz/create_quiz.html')

@login_required
def set_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)  # Ensure the quiz object is fetched by ID
    
    if request.method == 'POST':
        question_texts = request.POST.getlist('question_text')
        option_a = request.POST.get('option_a')
        option_b = request.POST.get('option_b')
        option_c = request.POST.get('option_c')
        option_d = request.POST.get('option_d')
        correct_option = request.POST.get('correct_option')

        for i in range(len(question_texts)):
            Question.objects.create(
                quiz=quiz,
                question_no=i + 1,
                text=question_texts[i],
                option_a=option_a[i],
                option_b=option_b[i],
                option_c=option_c[i],
                option_d=option_d[i],
                correct_option=correct_option
            )
        
        messages.success(request, "Quiz questions created successfully!")
        return redirect('quiz_home') 

    return render(request, 'quiz/set_questions.html', {'quiz': quiz})
