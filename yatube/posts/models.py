<<<<<<< HEAD
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_posts')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, \
        related_name='group_posts', blank=True, null=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    text = models.TextField()
    created = models.DateTimeField("date published", auto_now_add=True, db_index=True)
    
    def __str__(self):
        return self.text
        

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'], name='unique relationship'),
        ]
=======
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_posts')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, \
        related_name='group_posts', blank=True, null=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    text = models.TextField()
    created = models.DateTimeField("date published", auto_now_add=True, db_index=True)
    
    def __str__(self):
        return self.text
        

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'], name='unique relationship'),
        ]
>>>>>>> e00ceddaa1758d008aea9fd3ff70b76728ca2368
