from rest_framework.fields import DateTimeField

from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
        }


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError({'detail': 'Invalid or already revoked token'})



class UserProfileListSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'following_count', 'followers_count']

    def get_following_count(self, obj):
        return obj.follower_fl.count()

    def get_followers_count(self, obj):
        return obj.following_fl.count()


class FollowSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format('%d-%m-%Y'))
    class Meta:
        model = Follow
        fields = ['id', 'created_at','follower_fl', 'following_fl']


class CommentLikeSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format('%d-%m-%Y'))
    class Meta:
        model = CommentLike
        fields = ['id', 'comment', 'like','user_comment_liker', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format('%d-%m-%Y'))
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user_commenter', 'text', 'parent', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['user_poster', 'image', 'video', 'description', 'hashtags', 'created_at', 'comments', 'likes_count',
                  'comments_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

class UserProfileDetailSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'bio', 'image', 'website', 'posts']


class StorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format('%d-%m-%Y'))

    class Meta:
        model = Story
        fields = ['id', 'user_story', 'image', 'video', 'created_at']


class SaveItemSerializer(serializers.ModelSerializer):
    save_user = PostSerializer(read_only=True)
    post = PostSerializer()
    class Meta:
        model = SaveItem
        fields = ['id', 'post', 'save_user']


class SaveSerializer(serializers.ModelSerializer):
    save_posts = SaveItemSerializer(many=True, read_only=True)
    user = UserProfileListSerializer(read_only=True)
    created_date = serializers.DateTimeField(format('%d-%m-%Y'))
    class Meta:
        model = Save
        fields = ['id', 'user', 'created_date', 'save_posts']


class PostLikeSerializer(serializers.ModelSerializer):
    user_post_liker = UserProfileListSerializer()
    created_at = serializers.DateTimeField(format('%d-%m-%Y'))

    class Meta:
        model = PostLike
        fields = ['id', 'user_post_liker', 'post', 'like', 'created_at']




