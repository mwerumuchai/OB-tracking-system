from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Officer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    badge_no = models.IntegerField(blank=False)
    rank = models.TextField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:

        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    instance.profile.save()

class CriminalProfile(models.Model):
    criminal_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True)
    criminal_id = models.IntegerField(blank=False)
    # phone_number = models.PhoneNumberField(max_length=10, null=True)
    criminal_image = models.ImageField(upload_to = 'criminalphotos/')
    crime_committed = models.CharField(max_length=500)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.criminal_id

class OccurrenceBook(models.Model):
    ob_no = models.IntegerField(blank=False)
    ref_no = models.IntegerField(blank=True)
    case_file_no = models.IntegerField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=250, blank=False)
    nature_of_occurence = models.CharField(max_length=250, blank=False)
    badge_no = models.ForeignKey(Officer, on_delete=models.CASCADE)
    crime_committed = models.ForeignKey(CriminalProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.ob_no

    class Meta:
        ordering = ['-date_posted']

class Crime(models.Model):
    crime_type = models.TextField(max_length=500, blank=False)
    crime_description = models.CharField(blank=False,max_length=500)

    def __str__(self):
        return self.crime_type


class Report(models.Model):
    reporter_name = models.TextField(max_length=150, blank=True)
    reporter_id = models. IntegerField(blank=True)
    report_description = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Booking(models.Model):
    criminal_name = models.ForeignKey(CriminalProfile, on_delete=models.CASCADE)
    badge_no = models.ForeignKey(Officer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crime_committed = models.ForeignKey(OccurrenceBook, on_delete=models.CASCADE)

    def __str__(self):
        return self.criminal_name + ' : '+self.badge_no
