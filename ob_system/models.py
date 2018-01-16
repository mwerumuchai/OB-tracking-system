from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

import datetime as dt

# Create your models here.


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    badge_no = models.IntegerField(blank=False, null=True)

    rank = models.TextField(max_length=50)

    email_confirmed = models.BooleanField(default=False)

    # ob_no = models.ForeignKey(OccurrenceBook)

    class UserFullName(User):
        class Meta:
            proxy = True

        def __unicode__(self):
            return self.get_full_name()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:

        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    instance.profile.save()


class CriminalProfile(models.Model):

    name = models.CharField(max_length=100)

    id_no = models.IntegerField(null=True)

    dob = models.DateField()

    image = models.ImageField(upload_to='criminal profile pictures/', blank=True)

    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Crime(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Report(models.Model):

    name = models.CharField(max_length=100)

    id_no = models.IntegerField()

    ref_no = models.CharField(max_length=150, blank=True)

    case_file_no = models.CharField(max_length=150, blank=True)

    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)

    crime_description = models.TextField()

    time = models.TimeField()

    pub_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def current_day_reports(cls):
        day = dt.date.today()

        reports = cls.objects.filter(pub_date__date=day)

        return reports

    def __str__(self):

        return self.name


# A_O stands for Arresting Officer

class Booking(models.Model):

    a_o_name = models.CharField(max_length=100)

    a_o_badge_no = models.IntegerField()

    criminal = models.ForeignKey(CriminalProfile, on_delete=models.CASCADE)

    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)

    crime_description = models.TextField()

    time = models.TimeField()

    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.a_o_name

    @classmethod
    def current_day_bookings(cls):
        day = dt.date.today()

        bookings = cls.objects.filter(pub_date__date=day)

        return bookings


class Remark(models.Model):

    report = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True)

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, blank=True)

    remarks = models.TextField()

    sign = models.CharField(max_length=100, blank=True)


class OccurrenceBook(models.Model):

    bookings = models.ForeignKey(Booking, on_delete=models.CASCADE)

    reports = models.ForeignKey(Report, on_delete=models.CASCADE)

    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pub_date

    @classmethod
    def current_day_ob(cls):

        day = dt.date.today()

        records = cls.objects.filter(pub_date__date=day)

        return records

    @classmethod
    def archives(cls, date):

        archive = cls.objects.filter(pub_date__date=date)

        return archive


class Archive(models.Model):

    bookings = models.ForeignKey(Booking, on_delete=models.CASCADE)

    reports = models.ForeignKey(Report, on_delete=models.CASCADE)

    pub_date = models.DateField(auto_now_add=True)

    @classmethod
    def search_by_pub_date(cls, search_term):

        reports = cls.objects.filter(pub_date__icontains=search_term)

        return reports
