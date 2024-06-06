from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from .forms import CommentForm, ContactForm
from .models import Post, Comment, Category

def all_posts(request):
    all_posts = Post.objects.filter(status='published')  # Query all blog posts
    context = {
        'all_posts': all_posts,
    }
    return render(request, 'blog/all_posts.html', context)

def category_posts(request, Meditazione):
    category = get_object_or_404(Category, name=Meditazione)
    posts = Post.objects.filter(category=Meditazione)
    context = {
        'category': category,
        'posts':posts,
    }
    return render(request, 'blog/category_posts.html', context)

def latest_posts(request):
    latest_posts = Post.objects.order_by('-created_at')[:4]
    context = {
        'latest_posts': latest_posts,
    }
    return render(request, 'blog/latest_posts.html', context)

def third_post(request):
    try:
        third_post = Post.objects.all().order_by('created_at')[2]
    except IndexError:
        third_post = None
    context = {
        'third_post': third_post,
    }
    return render(request, 'blog/third_post.html', context)

def top_commented_posts(request):
    top_commented_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
    context = {
        'top_commented_posts': top_commented_posts,
    }
    return render(request, 'blog/top_commented_posts.html', context)

def combined_view(request):
    all_posts = Post.objects.all()
    meditazione_category = Category.objects.get(name='Meditazione')
    category_posts = Post.objects.filter(category=meditazione_category)
    latest_posts = Post.objects.order_by('created_at')[:4]
    
    try:
        third_post = all_posts.order_by('created_at')[2]
    except IndexError:
        third_post = None
    
    top_commented_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]
    
    context = {
        'all_posts': all_posts,
        'category_posts': category_posts,
        'latest_posts': latest_posts,
        'third_post': third_post,
        'top_commented_posts': top_commented_posts,
    }
    
    return render(request, 'blog/home.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send an email or save the message to the database
            try:
                # Try to send the email
                send_mail(
                    f'Message from {name}',
                    message,
                    email,
                    [settings.EMAIL_HOST_USER],  # Replace with your email
                )
                return render(request, 'blog/contact_success.html')
            except Exception as e:
                # Log the error
                print(f'Error sending email: {e}')
                return render(request, 'blog/contact_error.html')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.data['upload']
        file_name = default_storage.save(file_obj.name, file_obj)
        file_url = default_storage.url(file_name)
        return Response({'url': file_url}, status=status.HTTP_201_CREATED)
