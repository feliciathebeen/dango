from django.db import models
from accounts.models import User
from sparta_market import settings


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    view_count = models.PositiveIntegerField(default=0)  # 조회수 필드 추가
    hashtags = models.ManyToManyField("Hashtag", blank=True, related_name='article_hashtag')

    def like_count(self):
        return self.like_users.count()  # 찜수 계산


class Hashtag(models.Model):
    content = models.TextField(unique=True)

    def __str__(self):
        return self.content


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class ArticleLike(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="likes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes"
    )