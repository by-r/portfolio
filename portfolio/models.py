from django.db import models
from django.core.exceptions import ValidationError

class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    about_text = models.TextField()
    email = models.EmailField()
    linkedin_url = models.URLField()
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and Profile.objects.exists():
            raise ValidationError("Only one profile can be created")
        super().save(*args, **kwargs)

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.CharField(max_length=20)  # Format: "9/2023"
    start_date_month = models.CharField(max_length=20)  # Format: "9/2023"
    start_date_year = models.CharField(max_length=20)  # Format: "9/2023"
    end_date = models.CharField(max_length=20)    # Format: "Current" or "12/2022"
    end_date_month = models.CharField(max_length=20, blank=True, null=True)    # Format: "Current" or "12/2022"
    end_date_year = models.CharField(max_length=20, blank=True, null=True)    # Format: "Current" or "12/2022"
    description = models.TextField()  # Use newlines for bullet points
    
    def __str__(self):
        return self.position
    
class SkillCategory(models.Model):
    name = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)  # For sorting

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name = 'Skill Category'
        verbose_name_plural = 'Skill Categories'

class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name