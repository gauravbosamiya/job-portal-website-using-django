from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class StudentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=False, blank=False)
    # image = models.ImageField(upload_to='images/', null=False, blank=False)
    image = models.FileField()
    gender = models.CharField(max_length=15, null=False, blank=False)
    type = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return self.user.username


class Recruiter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=False, blank=False)
    # image = models.ImageField(upload_to='images/', null=False, blank=False)
    image = models.FileField()
    gender = models.CharField(max_length=15, null=False, blank=False)
    company = models.CharField(max_length=100, null=False, blank=False)
    type = models.CharField(max_length=15, null=False, blank=False)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    salary = models.FloatField(max_length=100)
    # image = models.ImageField(upload_to='images/')
    image = models.FileField()
    description = models.CharField(max_length=400)
    experience = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    skills = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Applicant(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    resume = models.FileField(null=True)
    applydate = models.DateField()

    def __str__(self):
        return self.job.title


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
