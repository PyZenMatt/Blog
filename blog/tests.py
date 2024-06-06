from django.test import TestCase
from django.shortcuts import render, get_object_or_404
from .models import Category, Post

def category_posts(request, Meditazione):
    print("Meditazione parameter:", Meditazione)  # Debugging line
    category = get_object_or_404(Category, name=Meditazione)
    posts = Post.objects.filter(category=Meditazione)
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category_posts.html', context)


# Create your tests here.
