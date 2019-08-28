from django.contrib.auth.models import AbstractUser
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('User', 'User'),
    )
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=100, null=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)
    address = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email', 'user_type', 'address', 'phone_number']

    def __str__(self):
        return self.username


class Snippet(models.Model):
    READ_OPTIONS = (
        ('YES', 'YES'),
        ('NO', 'NO')
    )
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey(User, related_name='snippets', on_delete=models.CASCADE)
    is_allowed_to_read = models.CharField(choices=READ_OPTIONS, max_length=50, default='YES')


    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title
