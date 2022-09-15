from django.db import models

# Create your models here.


class JobRole(models.Model):
    job_role = models.CharField(max_length=150, unique=True)
    skills = models.TextField()
