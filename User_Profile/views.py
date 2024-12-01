from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quiz.models import Quiz 
from participation.models import Participant
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def profile_home(request):
    """
    View to display the user's profile homepage.

    This view renders the main profile page for the logged-in user.

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate the response.

    Returns
    -------
    HttpResponse
        A rendered response displaying the profile home page.
    """
    return render(request, 'User_Profile/profile_home.html')

@login_required
def user_stats(request):
    """
    View to display the user's statistics, including their ranking and scores.

    This view calculates and displays the user's rank based on the total 
    score from all participations, the number of participations, and 
    quizzes created by the user.

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate the response.

    Returns
    -------
    HttpResponse
        A rendered response displaying the user's statistics, 
        including rank, total score, and quiz count.
    """
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
    """
    View to display the user's information (username, email, bio, location, and profile picture).

    This view retrieves the user's profile information and displays it.

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate the response.

    Returns
    -------
    HttpResponse
        A rendered response displaying the user's profile information.
    """
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
    """
    View to handle updating the user's profile settings.

    This view allows the logged-in user to update their username, email, bio, 
    location, date of birth, and profile picture. If a POST request is made, 
    the user's information is updated and a success message is shown.

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate the response, containing form data for updating user settings.

    Returns
    -------
    HttpResponse
        A rendered response displaying the settings page with updated user information.
    """
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
