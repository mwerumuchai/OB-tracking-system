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

    @classmethod
    def officer_profile(cls, badge_no):

        profile = cls.objects.get(badge_no=badge_no)

        return profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:

        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    instance.profile.save()


class CriminalProfile(models.Model):

    name = models.CharField(max_length=100)

    id_no = models.IntegerField(null=False, blank=False)

    dob = models.DateField()

    image = models.ImageField(upload_to='criminal profile pictures/', blank=True)

    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @classmethod
    def criminal_profile(cls, id_no):

        profile = cls.objects.get(id_no=id_no)

        return profile


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

    def __str__(self):
        return self.name

    @classmethod
    def current_day_reports(cls):
        day = dt.date.today()

        reports = cls.objects.filter(pub_date__date=day)

        return reports

    @classmethod
    def search_by_pub_date(cls, search_term):

        reports = cls.objects.get(pub_date__icontains=search_term)

        return reports


# # A_O stands for Arresting Officer

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

    @classmethod
    def single_criminal_booking(cls, criminal):

        bookings = cls.objects.filter(id=criminal)

        return bookings

    @classmethod
    def search_by_pub_date(cls, search_term):

        reports = cls.objects.get(pub_date__icontains=search_term)

        return reports


class Remark(models.Model):

    report = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True, null=True)

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, blank=True, null=True)

    remarks = models.TextField()

    sign = models.CharField(max_length=100, blank=True)

    # def __str__(self):
    #     return self.

    @classmethod
    def single_remark(cls):

        remark = cls.objects.filter()

        return remark


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


class CashBail(models.Model):

    p_station = models.CharField(max_length=250)

    sum = models.IntegerField()

    court_name = models.CharField(max_length=250)

    court_date = models.DateField()

    court_time = models.TimeField()

    current_date = models.DateField()

    current_time = models.TimeField()

    criminal = models.ForeignKey(CriminalProfile, on_delete=models.CASCADE)

    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)


