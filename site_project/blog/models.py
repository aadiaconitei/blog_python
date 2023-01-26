from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator
from datetime import date, datetime
from ckeditor.fields import RichTextField

# Create your models here.
STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class MyModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(MyModel):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('homepage')

    class Meta:
        db_table = 'categories'
        verbose_name_plural = "Categories"


class Post(MyModel):
    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True, blank=True, upload_to="headers")
    title_tag = models.CharField(max_length=255, default="My Blog Django")
    # slug = models.SlugField(max_length=200, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, default=1)
    body = RichTextField(blank=True, null=True)
    post_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    snippet = models.CharField(max_length=255, default='Click link above to read blog post')
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_posts')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + '|' + str(self.owner)

    def get_absolute_url(self):
        return reverse('posts')


class Comment(MyModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post)

