from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
import uuid
from django.utils.translation import gettext_lazy as _

# Create your models here.

def validate_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError(
            _('You must be at least 18 years old.'),
            code='invalid',
        )



class AccoutUser(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE , related_name= "account_user")
    name =models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True, validators=[validate_age])
    

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    author = models.ForeignKey(AccoutUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    users = models.ForeignKey(AccoutUser, on_delete=models.CASCADE, related_name="like_users")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'users')

    def save(self, *args, **kwargs):
        if self.post.is_public:
            super(Like, self).save(*args, **kwargs)
        else:
            raise ValidationError(_('This post is not public.'))

    @classmethod
    def get_likes_for_post(cls, post_id):
        return cls.objects.filter(post_id=post_id).select_related('user')


