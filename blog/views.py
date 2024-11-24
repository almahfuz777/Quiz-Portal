from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from core.models import User
from django.contrib.auth.decorators import login_required

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/blog_list.html', {'blogs': blogs})

@login_required(login_url='login')
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        blog = Blog.objects.create(title=title, content=content, author=request.user)
        return redirect('blog_list')
    return render(request, 'blog/create_blog.html')

def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'blog/blog_detail.html', {'blog': blog})
