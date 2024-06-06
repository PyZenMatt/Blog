from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null='True')
    text = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    title = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    preview_image = models.ImageField(upload_to='preview_images/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    hero_slider = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.preview_image:
            img = Image.open(self.preview_image.path)
            if img.height > 300 or img.width > 300:
                output_size = (150, 150)
                img.thumbnail(output_size)
                img.save(self.preview_image.path)

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comments.count()  # This counts the number of comments associated with the post


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'



