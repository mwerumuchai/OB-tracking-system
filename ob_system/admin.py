from django.contrib import admin
from .models import CriminalProfile, OccurrenceBook, Crime, Report, Booking,Remark,Archive,CashBail

admin.site.register(CriminalProfile)
admin.site.register(OccurrenceBook)
admin.site.register(Crime)
admin.site.register(Report)
admin.site.register(Booking)
admin.site.register(Remark)
admin.site.register(Archive)
admin.site.register(CashBail)
