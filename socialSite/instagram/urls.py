from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .views import *
from django.urls import path

router = DefaultRouter()
router.register(r'save-items', SaveItemViewSet, basename='save-items')
router.register(r'saves', SaveViewSet, basename='saves')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('users/', UserProfileListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user-detail'),

    path('follows/', FollowListAPIView.as_view(), name='follow-list'),

    path('posts/', PostAPIView.as_view(), name='post-list'),

    path('post-likes/', PostLikeAPIView.as_view(), name='post-like-list'),

    path('comments/', CommentListAPIView.as_view(), name='comment-list'),

    path('comment-likes/', CommentLikeListAPIView.as_view(), name='comment-like-list'),

    path('stories/', StoryListCreateAPIView.as_view(), name='story-list'),

    path('', include(router.urls)),
]
