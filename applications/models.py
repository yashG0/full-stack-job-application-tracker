from django.conf import settings
from django.db import models


# Create your models here.
class Application(models.Model):
    class Status(models.TextChoices):
        APPLIED = "applied", "Applied"
        PHONE_SCREEN = "phone_screen", "Phone Screen"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    company = models.CharField(max_length=200)
    role_title = models.CharField(max_length=200)
    job_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.APPLIED,
    )
    applied_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.role_title} at {self.company}"


class StatusHistory(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="status_history",
    )
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["changed_at"]

    def __str__(self):
        return (
            f"{self.application} — {self.old_status or 'created'} → {self.new_status}"
        )


class Contact(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    role = models.CharField(
        max_length=100, blank=True, help_text="e.g. Recruiter, Referral"
    )

    def __str__(self):
        return self.name
