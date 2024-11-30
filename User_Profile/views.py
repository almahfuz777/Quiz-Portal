from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quiz.models import Quiz 
from participation.models import Participant
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def profile_home(request):
    return render(request, 'User_Profile/profile_home.html')

@login_required
def user_stats(request):
    user = request.user

    # Get all participations for ranking
    all_participations = Participant.objects.all().order_by('-score')

    # Calculate user rank
    user_rank = 1
    for index, participant in enumerate(all_participations):
        if participant.user == user:
            user_rank = index + 1
            break

    # Get user-specific participations
    participations = Participant.objects.filter(user=user)

    # Total score from all participations
    total_score = sum(part.score for part in participations)

    # Get quizzes created by the user
    created_quizzes = Quiz.objects.filter(created_by=user)

    context = {
        'created_quizzes_count': created_quizzes.count(),
        'participations_count': participations.count(),
        'total_score': total_score,
        'user_rank': user_rank,
    }
    return render(request, 'User_Profile/user_stats.html', context)

@login_required
def user_info(request):
    user = request.user
    profile = user.profile  # Access the related Profile object

    context = {
        'username': user.username,
        'email': user.email,
        'bio': profile.bio,
        'location': profile.location,
        'date_of_birth': profile.date_of_birth,
        'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
    }
    return render(request, 'User_Profile/user_info.html', context)

@login_required
def settings(request):
    user = request.user
    profile = user.profile
    message = None

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_bio = request.POST.get('bio')
        new_location = request.POST.get('location')
        new_date_of_birth = request.POST.get('date_of_birth')
        profile_picture = request.FILES.get('profile_picture')

        # Update user information
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        user.save()

        # Update profile information
        if new_bio:
            profile.bio = new_bio
        if new_location:
            profile.location = new_location
        if new_date_of_birth:
            profile.date_of_birth = new_date_of_birth
        if profile_picture:
            profile.profile_picture = profile_picture
        profile.save()

        message = "Profile updated successfully!"

    context = {
        'username': user.username,
        'email': user.email,
        'bio': profile.bio,
        'location': profile.location,
        'date_of_birth': profile.date_of_birth,
        'message': message,
    }
    return render(request, 'User_Profile/settings.html', context)
