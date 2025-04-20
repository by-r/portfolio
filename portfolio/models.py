from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Experience(models.Model):

    role = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    company_url = models.URLField(max_length=200)
    startdate = models.DateField(auto_now=False, auto_now_add=False)
    enddate = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"

    def __str__(self):
        return self.name

class ResumeUser(AbstractUser):
    experience = models.ForeignKey(Experience, verbose_name="", on_delete=models.CASCADE)
    