from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from datetime import timedelta, datetime
from django.utils.timezone import make_aware
from .models import Quiz, Question
from core.models import Tag
from participation.models import Participant

@login_required
def quiz_home(request):
    """
    Renders the quiz homepage, displaying available quizzes and tags, 
    and applying optional filters such as quiz type, tags, and availability.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template displaying quizzes.
    """
    quizzes = Quiz.objects.all()
    tags = Tag.objects.all()
    quiz_type = request.GET.get('quiz_type')
    tag = request.GET.get('tag')
    available_only = request.GET.get('available_only')

    # Apply filters if present
    if 'quiz_type' in request.GET and request.GET['quiz_type']:
        quizzes = quizzes.filter(quiz_type=request.GET['quiz_type'])
    
    if 'tag' in request.GET and request.GET['tag']:
        quizzes = quizzes.filter(tags__id=request.GET['tag'])

    if available_only:  # Check if the "available only" checkbox is checked
        quizzes = quizzes.filter(expiry_date__gte=now())
    
    # Format duration into a readable format
    for quiz in quizzes:
        # Convert the duration (timedelta) to hours, minutes, seconds
        duration_seconds = int(quiz.duration.total_seconds())
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        seconds = duration_seconds % 60
        quiz.formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
        
    # Najifa's part for feedback button
    participant = Participant.objects.filter(user=request.user).first()
    participant_id = participant.participant_id if participant else None

    return render(request, 'quiz/quiz_home.html', {
        'quizzes': quizzes,
        'tags': tags,
        'participant_id': participant_id,  # Pass the participant_id safely
    })

@login_required
def create_quiz(request):
    """
    Handles the creation of a new quiz. 

    This view allows the user to provide details for the quiz such as 
    the title, description, type, password (if private), duration, 
    expiry date, and associated tags. It validates the input and creates 
    the quiz object in the database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirect to the 'set_questions' view or render the quiz creation form.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        quiz_type = request.POST.get('quiz_type')
        password = request.POST.get('password') if quiz_type == 'private' else None
        duration_hours = int(request.POST.get('duration_hours', 0))
        duration_minutes = int(request.POST.get('duration_minutes', 0))
        duration_seconds = int(request.POST.get('duration_seconds', 0))
        expiry_date = request.POST.get('expiry_date')
        tags = request.POST.getlist('tags')
        new_tags = request.POST.getlist('new_tags')
        can_view_score = request.POST.get('can_view_score') == 'on'

        # Validate duration and expiry_date formats
        try:
            duration_timedelta = timedelta(hours=duration_hours, minutes=duration_minutes, seconds=duration_seconds)
        except ValueError:
            return HttpResponse("Invalid duration format.", status=400)

        # Handle expiry_date (if empty, set to None)
        if expiry_date:
            try:
                expiry_date = make_aware(datetime.strptime(expiry_date, "%Y-%m-%dT%H:%M"))
            except ValueError:
                return HttpResponse("Invalid expiry date format.", status=400)
        else:
            expiry_date = None  # Set to None if not provided
        try:
            quiz = Quiz.objects.create(
                title=title,
                description=description,
                quiz_type=quiz_type,
                password=password,
                duration=duration_timedelta,
                expiry_date=expiry_date,
                can_view_score_immediately=can_view_score,
                created_by=request.user,  # Associate the quiz with the user
            )
        except ValidationError as e:
            return HttpResponse(e.message, status=400)
        
        # Handle tag creation or selection
        if new_tags:
            # Ensure new_tags is a string before calling split
            if isinstance(new_tags, str):
                for tag_name in new_tags.split(','):
                    tag_name = tag_name.strip()  # Clean up any extra spaces
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    quiz.tags.add(tag)
            elif isinstance(new_tags, list):  # If it's already a list (multiple tags)
                for tag_name in new_tags:
                    tag_name = tag_name.strip()  # Clean up any extra spaces
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    quiz.tags.add(tag)
        else:
            # Add selected tags to the quiz
            for tag_id in tags:
                tag = Tag.objects.get(id=tag_id)
                quiz.tags.add(tag)

        quiz.save()
        
        messages.success(request, f'Quiz "{quiz.title}" created successfully. Now, you can set questions.')
        return redirect('set_questions', quiz_id=quiz.quiz_id)
    
    tags = Tag.objects.all()  # Fetch all tags
    return render(request, 'quiz/create_quiz.html', {'tags': tags})

@login_required
def set_questions(request, quiz_id):
    """
    Handles the creation of questions for a quiz.

    This view allows the user to submit a list of questions, options, and 
    correct answers for the quiz. It validates the input and creates the 
    associated Question objects in the database.

    Args:
        request (HttpRequest): The HTTP request object.
        quiz_id (UUID): The unique identifier for the quiz.

    Returns:
        HttpResponse: Redirects to the quiz home page or renders the set questions form.
    """
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
    
    if request.method == 'POST':
        question_texts = request.POST.getlist('question_text[]')
        options_a = request.POST.getlist('option_a[]')
        options_b = request.POST.getlist('option_b[]')
        options_c = request.POST.getlist('option_c[]')
        options_d = request.POST.getlist('option_d[]')
        correct_options = request.POST.getlist('correct_option[]')

        num_questions = len(question_texts)
        for i in range(num_questions):
            Question.objects.create(
                quiz=quiz,
                question_no=i + 1,
                text=question_texts[i],
                option_a=options_a[i],
                option_b=options_b[i],
                option_c=options_c[i],
                option_d=options_d[i],
                correct_option=correct_options[i],
            )
        
        messages.success(request, "Quiz questions created successfully!")
        return redirect('quiz_home') 

    return render(request, 'quiz/set_questions.html', {'quiz': quiz})
