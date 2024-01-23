from django.contrib import admin
from . models import StudentUser, Recruiter, Job, Applicant, Message
# Register your models here.

admin.site.register(StudentUser)
admin.site.register(Recruiter)
admin.site.register(Job)
admin.site.register(Applicant)
admin.site.register(Message)
