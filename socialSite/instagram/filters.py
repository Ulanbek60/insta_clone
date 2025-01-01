import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            'user_poster': ['exact'],
            'created_at': ['gte', 'lte'],
            'hashtag': ['icontains'],
        }