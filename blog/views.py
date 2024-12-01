from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from core.models import User
from django.contrib.auth.decorators import login_required

def blog_list(request):
    """
    View to display a list of all blogs.

    This view retrieves all the blog posts from the database and displays them
    in a list view.

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate the response.

    Returns
    -------
    HttpResponse
        A rendered response with a list of all blogs in the system.
    """
    blogs = Blog.objects.all()
    return render(request, 'blog/blog_list.html', {'blogs': blogs})

@login_required(login_url='login')
def create_blog(request):
    """
    View to handle the creation of a new blog post.

    This view allows a logged-in user to submit a new blog post via a form. 
    If the form is submitted via POST, a new blog post is created and the user 
    is redirected to the blog list page. If the form is displayed (GET request), 
    an empty form is shown to the user.

    Parameters
    ----------
    request : HttpRequest
        The request object containing the form data (if POST).

    Returns
    -------
    HttpResponse
        A response that either redirects to the blog list page (after creation)
        or renders the blog creation form.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        blog = Blog.objects.create(title=title, content=content, author=request.user)
        return redirect('blog_list')
    return render(request, 'blog/create_blog.html')

def blog_detail(request, id):
    """
    View to display the details of a single blog post.

    This view retrieves a specific blog post by its ID and displays it on 
    the blog detail page.

    Parameters
    ----------
    request : HttpRequest
        The request object used to generate the response.
    id : int
        The ID of the blog post to retrieve.

    Returns
    -------
    HttpResponse
        A rendered response containing the details of the specific blog post.
    """
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'blog/blog_detail.html', {'blog': blog})
