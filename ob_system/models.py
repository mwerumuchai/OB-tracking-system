from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    badge_no = models.IntegerField(blank=False)

    rank = models.TextField(max_length=50)

    email = models.EmailField()

    # ob_no = models.ForeignKey(OccurrenceBook)

    def __str__(self):

        return self.user.username

    def update_profile(selfsender, instance, created, **kwargs):

        if created:

            Profile.objects.create(user=instance)

        instance.profile.save()

