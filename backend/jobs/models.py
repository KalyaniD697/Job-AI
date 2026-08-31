from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    experience = models.CharField(max_length=255, blank=True)

    skills = models.JSONField(default=list, blank=True)

    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)

    contact_name = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)

    job_url = models.URLField(max_length=1000, blank=True)
    application_url = models.URLField(max_length=1000, blank=True)

    match_score = models.FloatField(null=True, blank=True)
    ai_summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company}"