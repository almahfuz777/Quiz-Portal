from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def chatbox_home(request):
    """
    View function for the chatbox home page.

    This view displays all the messages in the chatbox and allows authenticated 
    users to submit new messages. The messages are ordered by timestamp, and 
    new messages are added via a POST request.

    If the request method is POST, a new message is created and saved to the database.

    Parameters
    ----------
    request : HttpRequest
        The request object containing metadata about the request.

    Returns
    -------
    HttpResponse
        Renders the 'chatbox/chatbox_home.html' template with the list of messages
        or redirects to the same page after a new message is submitted.
    """
    # Fetch all messages, order by timestamp so the latest messages appear last
    messages = Message.objects.all().order_by('timestamp')
    
    if request.method == 'POST':
        # If the user submits a message, save it
        content = request.POST.get('content')
        if content:
            Message.objects.create(user=request.user, content=content)
        return redirect('chatbox_home')  # Redirect to the same page to reload the messages

    return render(request, 'chatbox/chatbox_home.html', {'messages': messages})
