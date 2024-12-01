from django.shortcuts import render
from participation.models import Participant

def leaderboard(request):
    """
    View function to display the leaderboard of participants.

    This view retrieves all participants from the database, orders them by their 
    score in descending order, and calculates their rank based on the order.

    It then renders the 'leaderboard/leaderboard.html' template with the 
    ordered participants.

    Parameters
    ----------
    request : HttpRequest
        The request object containing metadata about the request.

    Returns
    -------
    HttpResponse
        Renders the 'leaderboard/leaderboard.html' template with the list of participants.
    
    Notes
    -----
    The rank for each participant is dynamically calculated by enumerating through the
    sorted participants, with ranks starting from 1.
    """
    participants = Participant.objects.all().order_by('-score')  # Order by score in descending order

    # Calculate rank for each participant
    for i, participant in enumerate(participants):
        participant.rank = i + 1  # Rank starts from 1

    return render(request, 'leaderboard/leaderboard.html', {
        'participants': participants,
    })
