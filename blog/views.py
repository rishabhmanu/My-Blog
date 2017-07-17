from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post, Comment
from django.utils import timezone
from .forms import ContactForm, CommentForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required

def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/index.html', {'posts':posts})

def about(request):
    return render(request, 'blog/about.html', {})

def post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post.html', {'post':post})


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(name, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "blog/contact.html", {'form': form})

def success(request):
    return render(request, "blog/success.html", {})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, "blog/add_comment_to_post.html", {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post', pk=comment.post.pk)
