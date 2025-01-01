from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class UserProfile(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_image/', null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower_fl', verbose_name= 'подписчик')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following_fl', verbose_name= 'подписки')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.follower == self.following:
            raise ValidationError('Вы не можете подписаться на самого себя')

    def __str__(self):
        return f'{self.follower}, - {self.following}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_follow')
        ]


class Post(models.Model):
    user_poster = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.FileField(upload_to='post_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    hashtag = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_likes(self):
        likes = self.user_poster.all()
        if likes.exists():
            return  likes.count()
        return 0

    def __str__(self):
        return f'{self.image} - {self.description}, - {self.user_poster}'


class PostLike(models.Model):
    user_post_liker = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_post_liker', 'post'], name='unique_post_like')
        ]

    def __str__(self):
        return f'{self.post}, - {self.user_post_liker}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_commenter = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post}, - {self.user_commenter}'


class CommentLike(models.Model):
    user_comment_liker = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_comment_liker', 'comment'], name='unique_comment_like')
        ]

    def __str__(self):
        return f'{self.user_comment_liker}, - {self.comment}'


class Story(models.Model):
    user_story = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='story_images/', null=True, blank=True)
    video = models.FileField(upload_to='story_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Save(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='save_user')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.created_date}'


class SaveItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    save_user = models.ForeignKey(Save, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} - {self.post}'


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='image', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

# swagger
