from django.db import models

# Create your models here.


class Job(models.Model):
    job_id = models.ImageField(null=False, blank=False, unique=True)
    job_type = models.TextField(null=False, blank=False)
    location = models.TextField()
    description = models.TextField()
    title = models.TextField(null=False, blank=False)
    core_skills = models.TextField()
    soft_skills = models.TextField()
    company_name = models.CharField(max_length=200, null=True, blank=True)
    posted_date = models.DateField(null=True, blank=True)


class Question(models.Model):
    question = models.TextField(null=False, blank=False,  unique=True)
    tags = models.TextField(null=False, blank=False)


class Level(models.Model):
    name = models.TextField(null=False, blank=False, unique=True)


class Transcript(models.Model):
    vtt_file = models.TextField(null=False, blank=False, unique=True)


class Interviewer(models.Model):
    emp_id = models.IntegerField(null=False, blank=False, unique=True)
    name = models.TextField(null=False, blank=False)
    max_level = models.TextField(null=False, blank=False)


class Rating(models.Model):
    values = models.TextField(null=False, blank=False, unique=True)


class Candidate(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    mobile_number = models.CharField(max_length=30, null=False, blank=False)
    email = models.CharField(max_length=200, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    core_skills = models.TextField()
    soft_skills = models.TextField()
    past_company = models.TextField()
    years_of_exp = models.TextField(default=0)
    past_title = models.TextField()

    class Meta:
        unique_together = ('name', 'email')


class QuestionLevelRating(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=False, blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, blank=False)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=False, blank=False)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        unique_together = ('candidate', 'question', 'level', 'rating')


class Interview(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=False, blank=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=False, blank=False)
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE, null=False, blank=False)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=False, blank=False)
    result = models.TextField(null=False, blank=False)

    class Meta:
        unique_together = ('candidate', 'job', 'interviewer', 'level', 'result')
