from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Languages(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Libraries(models.Model):
    name = models.CharField(max_length=50)


class Project(models.Model):
    name = models.CharField(max_length=50)
    lang = models.CharField(max_length=50)
    live_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Experience(models.Model):
    role = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    company_url = models.URLField(max_length=200)
    startdate = models.DateField(auto_now=False, auto_now_add=False)
    enddate = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"

    def __str__(self):
        return self.role


class ExperienceLanguage(models.Model):
    exp_lang = models.CharField(max_length=50)
    
class Portfolio(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    experience = models.ManyToManyField(Experience, blank=True)
    languages = models.ManyToManyField(Languages, blank=True)
    libraries = models.ManyToManyField(Libraries, blank=True)
    project = models.ManyToManyField(Project, blank=True)