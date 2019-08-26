from django.contrib.auth.models import AbstractUser
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)
    address = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['address', 'phone_number']

    def __str__(self):
        return self.first_name



class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey(User, related_name='snippets', on_delete=models.CASCADE)


    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title
