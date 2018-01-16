from django.contrib import admin
from .models import Profile, CriminalProfile, OccurrenceBook, Crime, Report, Booking

admin.site.register(Profile)
admin.site.register(CriminalProfile)
admin.site.register(OccurrenceBook)
admin.site.register(Crime)
admin.site.register(Report)
admin.site.register(Booking)
