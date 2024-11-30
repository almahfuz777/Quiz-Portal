from django.shortcuts import render
from participation.models import Participant

def leaderboard(request):
    """Fetches all participants and orders them by score in descending order"""
    participants = Participant.objects.all().order_by('-score')  # Order by score in descending order

    # Calculate rank for each participant
    for i, participant in enumerate(participants):
        participant.rank = i + 1  # Rank starts from 1

    return render(request, 'leaderboard/leaderboard.html', {
        'participants': participants,
    })
