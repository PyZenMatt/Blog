from django.urls import path
from blog.views import post_detail, all_posts, combined_view, post_detail, top_commented_posts
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.combined_view, name='home'),
    path('all_posts', views.all_posts, name='all_posts'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('latest_posts/', views.latest_posts, name='latest_posts'),
    path('top_commented_posts', views.top_commented_posts, name='top_commented_posts'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
   
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)